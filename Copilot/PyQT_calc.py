# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQT_calc.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from builtins import print

# pip install pyqt5 # инсталюємо все необходимое для работы программы
# pip install pyqt5-tools # инсталюємо все необходимое для работы программы
# команда для переходу в папку з файлом з кодом: cd C:\Users\Олександр\Desktop\Копіпаста\Копіпаста\Copilot
# команда для перетворення файлу в код: 'pyuic5 FileName.ui -o FileName.py'
    # pyuic5 PyQT_calc.ui -o PyQT_calc.py
    # (але спершу необхідно перейти в папку з файлом з кодом)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox as MsgBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 400)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Ukrainian, QtCore.QLocale.Ukraine))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 300, 50))
        self.label.setStyleSheet("background-color: rgb(159, 159, 159);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 14pt \"Verdana\";")
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.btn_0 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_0.setGeometry(QtCore.QRect(0, 330, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_0.setFont(font)
        self.btn_0.setObjectName("btn_0")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.btn_0)
        self.btn_1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_1.setGeometry(QtCore.QRect(0, 260, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_1.setFont(font)
        self.btn_1.setObjectName("btn_1")
        self.buttonGroup.addButton(self.btn_1)
        self.btn_4 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_4.setGeometry(QtCore.QRect(0, 190, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_4.setFont(font)
        self.btn_4.setObjectName("btn_4")
        self.buttonGroup.addButton(self.btn_4)
        self.btn_7 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_7.setGeometry(QtCore.QRect(0, 120, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_7.setFont(font)
        self.btn_7.setObjectName("btn_7")
        self.buttonGroup.addButton(self.btn_7)
        self.btn_mu = QtWidgets.QPushButton(self.centralwidget)
        self.btn_mu.setGeometry(QtCore.QRect(240, 120, 60, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_mu.setFont(font)
        self.btn_mu.setStyleSheet("background-color: rgb(193, 255, 206);")
        self.btn_mu.setObjectName("btn_mu")
        self.btn_9 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_9.setGeometry(QtCore.QRect(160, 120, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_9.setFont(font)
        self.btn_9.setObjectName("btn_9")
        self.btn_3 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_3.setGeometry(QtCore.QRect(160, 260, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_3.setFont(font)
        self.btn_3.setObjectName("btn_3")
        self.btn_6 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_6.setGeometry(QtCore.QRect(160, 190, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_6.setFont(font)
        self.btn_6.setObjectName("btn_6")
        self.btn_q = QtWidgets.QPushButton(self.centralwidget)
        self.btn_q.setGeometry(QtCore.QRect(240, 60, 60, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_q.setFont(font)
        self.btn_q.setStyleSheet("background-color: rgb(193, 255, 206);")
        self.btn_q.setObjectName("btn_q")
        self.btn_8 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_8.setGeometry(QtCore.QRect(80, 120, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_8.setFont(font)
        self.btn_8.setObjectName("btn_8")
        self.btn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_2.setGeometry(QtCore.QRect(80, 260, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_2.setFont(font)
        self.btn_2.setObjectName("btn_2")
        self.btn_5 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_5.setGeometry(QtCore.QRect(80, 190, 80, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_5.setFont(font)
        self.btn_5.setObjectName("btn_5")
        self.btn_mi = QtWidgets.QPushButton(self.centralwidget)
        self.btn_mi.setGeometry(QtCore.QRect(240, 190, 60, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_mi.setFont(font)
        self.btn_mi.setStyleSheet("background-color: rgb(193, 255, 206);")
        self.btn_mi.setObjectName("btn_mi")
        self.btn_pl = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pl.setGeometry(QtCore.QRect(240, 260, 60, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_pl.setFont(font)
        self.btn_pl.setStyleSheet("background-color: rgb(193, 255, 206);")
        self.btn_pl.setObjectName("btn_pl")
        self.btn_eq = QtWidgets.QPushButton(self.centralwidget)
        self.btn_eq.setGeometry(QtCore.QRect(160, 330, 140, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_eq.setFont(font)
        self.btn_eq.setStyleSheet("background-color: rgb(255, 206, 207);")
        self.btn_eq.setObjectName("btn_eq")
        self.btn_s1_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_s1_2.setGeometry(QtCore.QRect(160, 60, 40, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_s1_2.setFont(font)
        self.btn_s1_2.setStyleSheet("background-color: rgb(193, 255, 206);")
        self.btn_s1_2.setObjectName("btn_s1_2")
        self.btn_mu2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_mu2.setGeometry(QtCore.QRect(200, 60, 40, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_mu2.setFont(font)
        self.btn_mu2.setStyleSheet("background-color: rgb(193, 255, 206);")
        self.btn_mu2.setObjectName("btn_mu2")
        self.btn_s1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_s1.setGeometry(QtCore.QRect(120, 60, 40, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_s1.setFont(font)
        self.btn_s1.setStyleSheet("background-color: rgb(193, 255, 206);")
        self.btn_s1.setObjectName("btn_s1")
        self.btn_c = QtWidgets.QPushButton(self.centralwidget)
        self.btn_c.setGeometry(QtCore.QRect(80, 330, 80, 70))  # 160, 260, 80, 70
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_c.setFont(font)
        self.btn_c.setObjectName("btn_c")
        self.btn_del = QtWidgets.QPushButton(self.centralwidget)
        self.btn_del.setGeometry(QtCore.QRect(60, 60, 60, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_del.setFont(font)
        self.btn_del.setStyleSheet("background-color: rgb(193, 255, 206);")
        self.btn_del.setObjectName("btn_del")
        self.btn_del_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_del_2.setGeometry(QtCore.QRect(0, 60, 60, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        self.btn_del_2.setFont(font)
        self.btn_del_2.setStyleSheet("background-color: rgb(193, 255, 206);")
        self.btn_del_2.setObjectName("btn_del_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.addFunctions()
        self.isEqual = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "0"))
        self.btn_0.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_0.setText(_translate("MainWindow", "0"))
        self.btn_1.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_1.setText(_translate("MainWindow", "1"))
        self.btn_4.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_4.setText(_translate("MainWindow", "4"))
        self.btn_7.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_7.setText(_translate("MainWindow", "7"))
        self.btn_mu.setText(_translate("MainWindow", "*"))
        self.btn_9.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_9.setText(_translate("MainWindow", "9"))
        self.btn_3.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_3.setText(_translate("MainWindow", "3"))
        self.btn_6.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_6.setText(_translate("MainWindow", "6"))
        self.btn_q.setText(_translate("MainWindow", "/"))
        self.btn_8.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_8.setText(_translate("MainWindow", "8"))
        self.btn_2.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_2.setText(_translate("MainWindow", "2"))
        self.btn_5.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_5.setText(_translate("MainWindow", "5"))
        self.btn_mi.setText(_translate("MainWindow", "-"))
        self.btn_pl.setText(_translate("MainWindow", "+"))
        self.btn_eq.setText(_translate("MainWindow", "="))
        self.btn_s1_2.setText(_translate("MainWindow", ")"))
        self.btn_mu2.setText(_translate("MainWindow", "**"))
        self.btn_s1.setText(_translate("MainWindow", "("))
        self.btn_c.setStyleSheet(_translate("MainWindow", "background-color: rgb(220, 255, 232);\n"
                                                          "background-color: rgb(189, 217, 208);"))
        self.btn_c.setText(_translate("MainWindow", "."))
        self.btn_del.setText(_translate("MainWindow", "<--"))
        self.btn_del_2.setText(_translate("MainWindow", "del"))

    def addFunctions(self):  # призначення функцій кнопкам
        self.btn_0.clicked.connect(lambda: self.writeNumber(self.btn_0.text()))
        self.btn_1.clicked.connect(lambda: self.writeNumber(self.btn_1.text()))
        self.btn_2.clicked.connect(lambda: self.writeNumber(self.btn_2.text()))
        self.btn_3.clicked.connect(lambda: self.writeNumber(self.btn_3.text()))
        self.btn_4.clicked.connect(lambda: self.writeNumber(self.btn_4.text()))
        self.btn_5.clicked.connect(lambda: self.writeNumber(self.btn_5.text()))
        self.btn_6.clicked.connect(lambda: self.writeNumber(self.btn_6.text()))
        self.btn_7.clicked.connect(lambda: self.writeNumber(self.btn_7.text()))
        self.btn_8.clicked.connect(lambda: self.writeNumber(self.btn_8.text()))
        self.btn_9.clicked.connect(lambda: self.writeNumber(self.btn_9.text()))
        self.btn_c.clicked.connect(lambda: self.writeNumber(self.btn_c.text()))
        self.btn_s1.clicked.connect(lambda: self.writeNumber(self.btn_s1.text()))
        self.btn_s1_2.clicked.connect(lambda: self.writeNumber(self.btn_s1_2.text()))
        self.btn_pl.clicked.connect(lambda: self.writeNumber(self.btn_pl.text()))
        self.btn_mi.clicked.connect(lambda: self.writeNumber(self.btn_mi.text()))
        self.btn_mu2.clicked.connect(lambda: self.writeNumber(self.btn_mu2.text()))
        self.btn_q.clicked.connect(lambda: self.writeNumber(self.btn_q.text()))
        self.btn_mu.clicked.connect(lambda: self.writeNumber(self.btn_mu.text()))

        self.btn_eq.clicked.connect(lambda: self.result())
        self.btn_del.clicked.connect(lambda: self.delete())
        self.btn_del_2.clicked.connect(lambda: self.clear())

    def writeNumber(self, number):  # запис у поле вводу даних
        if self.isEqual and number.isdigit():
            self.isEqual = False
            self.label.setText("")
        else:
            self.isEqual = False
        if self.label.text() == "0":
            self.label.setText("")
        self.label.setText(self.label.text() + number)
        if self.label.text() == ".":
            self.label.setText("0.")

    def ErrBox(self, text, infoText="", detailText=""):  # вікно помилки
        msg = MsgBox()
        msg.setIcon(MsgBox.Warning)
        msg.setText(text)
        if not infoText == "":
            msg.setInformativeText(infoText)
        if not detailText == "":
            msg.setDetailedText(detailText)
        msg.setStandardButtons(MsgBox.Reset | MsgBox.Cancel | MsgBox.Ok)
        msg.setDefaultButton(MsgBox.Ok)
        msg.buttonClicked.connect(self.clickAction)
        msg.exec_()

    def clickAction(self, button):  # дії при натисканні кнопок вікна помилки
        # print(button.text())
        if button.text() == "OK":
            self.clear()
        elif button.text() == "Reset":
            self.clear()

    def result(self):
        # is error then show error message
        try:
            self.isEqual = True
            self.label.setText(str(eval(self.label.text())))
        except:
            # self.label.setText("Error")
            self.ErrBox("Помилкова операція!", "Очистити введенні данні?", "Перевірте правильність введених даних")

    def delete(self):
        self.label.setText(self.label.text()[:-1])

    def clear(self):
        self.label.setText("0")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
