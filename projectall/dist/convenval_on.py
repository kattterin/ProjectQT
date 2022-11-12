import sqlite3

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import QtCore, QtWidgets
from starculc import Ui_mainWindow
import datetime as dt


class Example(QMainWindow, Ui_mainWindow):

    def __init__(self, value):
        self.value = value
        super().__init__()
        self.setupUi(self)
        self.pole.addItems(list(value.keys()))
        self.pole2.addItems(list(value.keys()))
        self.radioButton_3.setChecked(1)
        self.lineoutput.setEnabled(False)
        self.take.clicked.connect(self.convert)
        self.lineinput.setText("1")
        self.con = sqlite3.connect('progectkonv.db')
        self.cur = self.con.cursor()
        dat = [int(i) for i in self.cur.execute('''SELECT DAT FROM currency
         ORDER BY id DESC LIMIT 1''').fetchall()[0][0].split('-')]
        self.dateEdit1.setMaximumDate(QtCore.QDate(*dat))
        self.dateEdit1.setDateTime(QtCore.QDateTime(QtCore.QDate(*dat)))
        self.pushButton_2.clicked.connect(self.clearhis)
        self.select_data()
        self.dateEdit1.setDisplayFormat("dd-MM-yyyy")
        self.dateEdit1.dateChanged.connect(self.changedata)
        self.changedata()
        self.pole.currentIndexChanged.connect(self.changedata)
        self.pole2.currentIndexChanged.connect(self.changedata)

    def changedata(self):
        self.dat1 = dt.date(*[int(i) for i in
                              self.cur.execute(f'''SELECT DAT FROM currency WHERE
                {self.value[self.pole.currentText()]} != -1
                         ORDER BY id LIMIT 1 ''').fetchall()[0][0].split('-')])

        self.dat2 = dt.date(*[int(i) for i in
                              self.cur.execute(f'''SELECT DAT FROM currency WHERE
                {self.value[self.pole2.currentText()]} != -1
                         ORDER BY id LIMIT 1 ''').fetchall()[0][0].split('-')])

        self.dateEdit1.setMinimumDate(self.dat1) if self.dat1 > self.dat2 else self.dateEdit1.setMinimumDate(self.dat2)

    def clearhis(self):
        self.cur.execute("DELETE FROM history")
        self.con.commit()
        self.select_data()

    # def closeEvent(self, event):
    #     self.con.close()

    def color_row(self, row, color):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row, i).setBackground(color)

    def select_data(self):
        self.res = self.cur.execute("""SELECT DAT, Val1, value1, just, Val2, value2, DAT2 FROM history""").fetchall()
        title = ['Дата запроса', 'Валюта', 'Значение', '', 'Валюта', 'Значение', "курс на дату..."]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.res[::-1]):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
            if self.tableWidget.rowCount() == 1:
                self.color_row(i, QColor(208, 208, 208, 150))

        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def convert(self):
        try:
            if self.radioButton_3.isChecked():  # точная дата
                d = self.dateEdit1.date().toPyDate()
                d = str(d).split("-")[2] + '-' + str(d).split("-")[1] + '-' + str(d).split("-")[0]
                valinput = self.cur.execute(f"""SELECT {self.value[self.pole.currentText()]} FROM currency
                        WHERE DAT == '{self.dateEdit1.date().toPyDate()}'
                        AND {self.value[self.pole.currentText()]} != -1""").fetchall()[0][0]

                valoutput = self.cur.execute(f"""SELECT {self.value[self.pole2.currentText()]} FROM currency
                                   WHERE DAT == '{self.dateEdit1.date().toPyDate()}' AND
                         {self.value[self.pole2.currentText()]} != -1""").fetchall()[0][0]

            elif self.radioButton_2.isChecked():  # month

                d = '-'.join([str(self.dateEdit1.date().year()), str(self.dateEdit1.date().month())]) if \
                    len(str(self.dateEdit1.date().month())) == 2 else \
                    '-'.join([str(self.dateEdit1.date().year()), '0' + str(self.dateEdit1.date().month())])

                valinput = round(float(self.cur.execute(f"""SELECT AVG({self.value[self.pole.currentText()]}) FROM currency
                                    WHERE DAT LIKE '{d}%'
                                     AND {self.value[self.pole.currentText()]} != -1""").fetchall()[0][0]), 4)

                valoutput = round(float(self.cur.execute(f"""SELECT AVG({self.value[self.pole2.currentText()]}) FROM currency
                                    WHERE DAT LIKE '{d}%' AND
                    {self.value[self.pole2.currentText()]} != -1""").fetchall()[0][0]), 4)
                d = d.split("-")[1] + '-' + d.split("-")[0]

            elif self.radioButton.isChecked():  # year
                d = (self.dateEdit1.date().year())

                valinput = round(float(self.cur.execute(f"""SELECT AVG({self.value[self.pole.currentText()]}) FROM currency
                                    WHERE DAT LIKE '{d}%' AND 
                        {self.value[self.pole.currentText()]} != -1""").fetchall()[0][0]), 4)

                valoutput = round(float(self.cur.execute(f"""SELECT AVG({self.value[self.pole2.currentText()]}) FROM currency
                                    WHERE DAT LIKE '{d}%' AND
                        {self.value[self.pole2.currentText()]} != -1""").fetchall()[0][0]), 4)

            valinput = valinput * float(self.lineinput.text())
            valoutput = round(float(valinput / valoutput), 4)
            self.lineoutput.setText(str(valoutput))
            dtt = dt.datetime.now()
            minut = str(dtt.minute) if len(str(dtt.minute)) == 2 else "0" + str(dtt.minute)
            dttime = "-".join([str(dtt.day), str(dtt.month), str(dtt.year)]) + ' ' + str(dtt.hour) + ':' + minut

            self.cur.execute(
                f"""INSERT INTO history(DAT, Val1, value1, Val2, value2, DAT2) VALUES('{dttime}', '{self.pole.currentText()}',
                            {self.lineinput.text()}, '{self.pole2.currentText()}', {self.lineoutput.text()}, '{d}')""")

            self.con.commit()
            self.select_data()

        except Exception:
            end_date = self.dateEdit1.date().toPyDate() + dt.timedelta(days=-1)
            self.dateEdit1.setDateTime(QtCore.QDateTime(QtCore.QDate(end_date)))
            self.convert()
