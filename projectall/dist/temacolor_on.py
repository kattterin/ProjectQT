import sqlite3
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5 import QtWidgets

from tema import Ui_MainWindow


class exam(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('progectkonv.db')
        self.cur = self.con.cursor()
        self.pushButton_3.clicked.connect(self.da)
        self.color2 = {}
        self.select_data()
        self.pushButton.clicked.connect(self.delet)
        self.spinBox.setMinimum(0)
        self.error = QMessageBox()
        self.error.setWindowTitle('Ошибка')
        self.error.setIcon(QMessageBox.Warning)

    def changeval(self):
        self.cur.execute(
            f"UPDATE something SET Fon = '{self.color2['fon']}', Text = '{self.color2['text']}',\
             Ramka = '{self.color2['ramka']}' WHERE nomer = {self.spinBox.value()}")
        self.con.commit()
        self.select_data()

    def download(self):
        if not self.spinBox.value():
            self.error.setText('Не выделен элемент, который можно было бы загрузить')
            self.error.exec_()
            return
        d = self.cur.execute(f'''SELECT * FROM something WHERE nomer = {self.spinBox.value()}''').fetchall()
        self.color2['fon'] = d[0][2]
        self.color2['text'] = d[0][3]
        self.color2['ramka'] = d[0][4]

    def delet(self):
        self.cur.execute(
            f"DELETE FROM something WHERE nomer == {self.spinBox.value()}")

        self.con.commit()
        self.select_data()

    def select_data(self):
        self.res = self.cur.execute("""SELECT nomer, title, Fon, Text, Ramka FROM something""").fetchall()
        for i, j in enumerate(self.res):
            self.cur.execute(f"UPDATE something SET nomer = {i + 1} WHERE title == '{j[1]}'")
            self.con.commit()
        self.res = self.cur.execute("""SELECT title, Fon, Text, Ramka FROM something""").fetchall()
        self.spinBox.setMaximum(len(self.res))

        title = ['Название', 'Фон', 'Текст', 'Рамки']
        self.tableWidget.setColumnCount(len(title))
        self.kol_vo = len(self.res)
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()
        # self.cur.execute(
        #     f"UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'something'")
        # self.con.commit()

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def da(self):
        self.error = QMessageBox()
        self.error.setWindowTitle('Ошибка')
        self.error.setIcon(QMessageBox.Warning)
        try:
            if not self.lineEdit.text():
                self.error.setText('Название не может быть пустым')
                self.error.exec_()
                return

            self.cur.execute(
                f"INSERT INTO something(nomer, title, Fon, Text, Ramka) VALUES(1, '{self.lineEdit.text()}',\
                 '{self.color2['fon']}',\
                 '{self.color2['text']}', '{self.color2['ramka']}')")

            self.con.commit()
            self.select_data()
        except Exception:
            self.error.setText('Такой слот уже есть в базе')
            self.error.exec_()
