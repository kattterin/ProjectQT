import csv
import sys

from PyQt5.QtWidgets import QMainWindow, QColorDialog, QWidget, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QApplication

from валюты import Ui_MainWindow
from convenval_on import Example
from graphic_on import Example2

from temacolor_on import exam

value = {'Доллар США': "US_dollar", "Украинская гривна": "Ukrainian_hryvnia", "Фунт стерлингов": "GBP",
         "Японская иена": "Japanese_yen", "Казахский тенге": "Kazakh_tenge",
         "Австралийский доллар": "Australian_dollar", "Датская крона": "Danish_krone",
         "Канадский доллар": "Canadian_dollar", "Норвежская крона": "Norwegian_krone",
         "Сингапурский доллар": "Singapore_dollar", "Турецкая лира": "Turkish_lira",
         "Швейцарский франк": "Swiss_frank", 'Российский рубль': "RUB"}

colorss2 = {'fon': '', 'text': "", "ramka": ""}

with open('typecolor.scv', 'r', newline='', encoding='utf-8') as f:
    reader = list(csv.reader(f, delimiter=';', quotechar='"'))[0]
    colorss2['fon'] = reader[0]
    colorss2['text'] = reader[1]
    colorss2['ramka'] = reader[2]


class AboutWindow(QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setWindowTitle('О программе')
        self.setLayout(QVBoxLayout(self))
        self.info = QLabel(self)
        self.info.setText('Создатель kattterina_i)')
        self.layout().addWidget(self.info)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.convenval)
        self.pushButton_2.clicked.connect(self.graphics)
        self.tema.clicked.connect(self.temacolor)
        self.w1 = exam()
        self.w2 = Example(value)
        self.w3 = Example2(value)
        self.returnwi1()
        self.colorssbutton = {'fon': '#ffffff', 'text': "#000000", "ramka": "#000000"}
        self.w1.label.setStyleSheet(
            "background-color: #ffffff;")
        self.w1.label_2.setStyleSheet(
            "background-color: #000000;")
        self.w1.label_3.setStyleSheet(
            "background-color: #000000;")

        self.about_window = AboutWindow()
        self.about_action.triggered.connect(self.about)

    def about(self):
        self.about_window.show()

    def returnwi1(self):
        global colorss2
        enironment = [self, self.w1, self.w2, self.w3]
        # self.colorssbutton = {'fon': 'ffffff', 'text': "#000000", "ramka": "#000000"}
        for i in enironment:
            MainWindow.setStyleSheet(i, f"""color: {colorss2['text']};\n
                                     background-color: {colorss2['fon']};\n
                                     border-width: 1px;\n
                                             border-style: solid;\n
                                             border-color: {colorss2['ramka']};""")
        self.w1.color2 = colorss2

    def temacolor(self):
        self.w1.show()

        def color1():
            color = QColorDialog.getColor()
            if color.isValid():
                if self.sender().text() == 'Фон':
                    self.w1.label.setStyleSheet(
                        "background-color: {}".format(color.name()))
                    self.colorssbutton['fon'] = color.name()
                elif self.sender().text() == 'Текст':
                    self.w1.label_2.setStyleSheet(
                        "background-color: {}".format(color.name()))
                    self.colorssbutton['text'] = color.name()

                elif self.sender().text() == 'Рамка':
                    self.w1.label_3.setStyleSheet(
                        "background-color: {}".format(color.name()))
                    self.colorssbutton['ramka'] = color.name()
                self.w1.color2 = self.colorssbutton

        def smena():
            global colorss2
            colorss2 = self.colorssbutton.copy()
            MainWindow.returnwi1(self)

        def changetema():
            self.w1.changeval()
            self.w1.color2 = self.colorssbutton
            # MainWindow.returnwi1(self)

        def changecolors():  # окно
            global colorss2
            self.w1.download()
            colorss2 = self.w1.color2
            MainWindow.returnwi1(self)

        self.w1.primenit.clicked.connect(smena)
        self.w1.fons.clicked.connect(color1)
        self.w1.texts.clicked.connect(color1)
        self.w1.ramks.clicked.connect(color1)
        self.w1.pushButton_2.clicked.connect(changecolors)
        self.w1.pushButton_4.clicked.connect(changetema)

    def convenval(self):
        # self.w2 = Example(value)

        self.w2.show()

        # MainWindow.close(self)
        def returnwi():
            self.w2.close()
            MainWindow.show(self)

        self.w2.pushButton_4.clicked.connect(returnwi)

    def graphics(self):
        # self.w3 = Example2(value)

        self.w3.show()

        def returnw2():
            self.w3.close()
            MainWindow.show(self)

        self.w3.pushButton_4.clicked.connect(returnw2)

    def closeEvent(self, event):
        global colorss2

        with open('typecolor.scv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(colorss2.values())

        self.w2.con.close()
        self.w3.con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
