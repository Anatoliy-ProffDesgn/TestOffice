from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Приклад програми з використанням PyQt5")
        self.setGeometry(300, 300, 500, 250)

        self.label = QtWidgets.QLabel(self)

        self.lb_name = QtWidgets.QLabel(self)
        self.lb_name.setText("Введіть, будь ласка, ваше ім'я:")
        self.lb_name.setFixedWidth(200)
        self.lb_name.move(10, 0)

        self.txt_name = QtWidgets.QLineEdit(self)
        self.txt_name.move(10, 25)
        self.txt_name.resize(160, 20)

        self.btn_ok = QtWidgets.QPushButton(self)
        self.btn_ok.setText("ОК")
        self.btn_ok.move(10, 50)
        self.btn_ok.clicked.connect(lambda: self.ok_clicked())

    def ok_clicked(self):
        # exit main_Wnd()
        # self.close()
        self.label.setText(self.txt_name.text())
        self.label.move(10, 80)
        self.label.adjustSize()


def main_Wnd():
    app = QApplication(sys.argv)  # передаємо системні параметри в програму
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())  # вихід з програми при натисканні кнопки закриття


if __name__ == '__main__':
    main_Wnd()
