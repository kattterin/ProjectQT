import sqlite3
from PyQt5.QtWidgets import QMainWindow
import pyqtgraph as pg
from pygraph import Ui_MainWindow


class Example2(QMainWindow, Ui_MainWindow):
    def __init__(self, value):
        self.value = value
        super().__init__()
        self.setupUi(self)
        self.comboBox.addItems(list(value.keys())[0:-1])

        self.con = sqlite3.connect('progectkonv.db')
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.graphik)
        self.checkBox.stateChanged.connect(self.change)
        self.checkBox_2.stateChanged.connect(self.change)
        self.a = False
        self.b = False
        self.d = False
        self.spinBox.setEnabled(self.a)
        self.spinBox_2.setEnabled(self.b)
        self.checkBox_2.setEnabled(self.a)
        self.comboBox.currentIndexChanged.connect(self.on_change)
        self.spinBox.valueChanged.connect(self.pors)
        self.checkBox_3.stateChanged.connect(self.axisc)

    def axisc(self):
        self.d = not self.d
        self.graphicsView.showGrid(x=self.d, y=self.d)

    def pors(self):
        self.on_change()
        if self.spinBox.value() == self.dat[0]:
            self.spinBox_2.setMinimum(self.dat[1])
        else:
            self.spinBox_2.setMinimum(1)

    def on_change(self):
        self.dat = [int(i) for i in
                    self.cur.execute(f'''SELECT DAT FROM currency WHERE {self.value[self.comboBox.currentText()]} != -1
                 ORDER BY id LIMIT 1 ''').fetchall()[0][0].split('-')]
        self.spinBox.setMinimum(self.dat[0])

    def change(self):
        if self.sender().text() == 'Год':
            self.on_change()
            if self.a:
                self.spinBox_2.setEnabled(False)
                self.checkBox_2.setChecked(False)
            self.a = not self.a
            self.spinBox.setEnabled(self.a)
            self.checkBox_2.setEnabled(self.a)
        if self.sender().text() == 'Месяц':
            self.b = not self.b
            self.spinBox_2.setEnabled(self.b)

    def graphik(self):
        symb = None
        self.graphicsView.clear()  # todo выход из диапазона
        if self.checkBox.isChecked():
            if self.checkBox_2.isChecked():
                d = str(self.spinBox.value()) + '-' + str(self.spinBox_2.value()) if len(
                    str(self.spinBox_2.value())) == 2 else \
                    str(self.spinBox.value()) + '-0' + str(self.spinBox_2.value())
                symb = "+"
            else:
                d = str(self.spinBox.value())

            valut = self.cur.execute(
                f"""SELECT DAT, {self.value[self.comboBox.currentText()]} FROM currency WHERE DAT LIKE '{d}%' AND
            {self.value[self.comboBox.currentText()]} != -1""").fetchall()
        else:
            valut = self.cur.execute(
                f"""SELECT DAT, {self.value[self.comboBox.currentText()]} FROM currency WHERE
                    {self.value[self.comboBox.currentText()]} != -1""").fetchall()
        xdict = {}
        x = [i + 15 for i in range(len(valut))]
        y = []
        for i in valut:
            xdict[x[valut.index(i)]] = i[0]
            y.append(i[1])
        if y and x:
            self.graphicsView.plot(x, y, pen='r', symbol=symb)
            styles = {"color": "#808080", "font-size": "20px"}
            self.graphicsView.setLabel("left", "Значение", **styles)
            self.graphicsView.setLabel("bottom", "Дата", **styles)
            self.stringaxis = pg.AxisItem(orientation='bottom')
            self.stringaxis.setTicks([xdict.items()])
            self.graphicsView.setAxisItems(axisItems={'bottom': self.stringaxis})

        else:
            self.statusbar.showMessage('Ничего не удалось построить')
