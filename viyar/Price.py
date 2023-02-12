# pip install pyqt5 # инсталюємо все необходимое для работы программы
# pip install pyqt5-tools # инсталюємо все необходимое для работы программы
# команда для переходу в папку з файлом з кодом: cd C:\Users\Олександр\Desktop\Копіпаста\Копіпаста\Copilot
# команда для перетворення файлу в код: 'pyuic5 FileName.ui -o FileName.py'
# pyuic5 PyQT_calc.ui -o PyQT_calc.py
# (але спершу необхідно перейти в папку з файлом з кодом)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox as MsgBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog
import mainWindow
import sys
import LoadPrice


class mWnd(QtWidgets.QMainWindow, mainWindow.Ui_mainWindow):
    # конструктор класу
    def __init__(self):
        super().__init__()  # виклик конструктора батьківського класу
        self.setupUi(self)  # ініціалізація інтерфейсу
        self.mMenu()  # виклик ініціалізації меню

    # метод іниціалізації меню
    def mMenu(self):
        self.updtPrice_.triggered.connect(self.updtPrice)  # прив`язка кнопки оновлення прайсу до методу updtPrice

    @QtCore.pyqtSlot()  # визначаємо слот для пункту меню
    # метод оновлення прайсу
    def updtPrice(self):
        msg = MsgBox.question(self,
                              'Повідомлення',
                              'Ви впевнені, що хочете оновити прайс?',
                              MsgBox.Yes | MsgBox.No,
                              MsgBox.Yes)
        if msg == MsgBox.Yes:
            self.statusbar.showMessage('Оновлення прайсу...')

            self.statusbar.showMessage('Оновлення прайсу завершено!')

def price_open():
    Price=LoadPrice.Read_CSV_FilePrice()
    print(Price)

# відкрити вікно з прайсом
def mainWindow_open():
    app = QtWidgets.QApplication(sys.argv)  # запуск програми
    window = mWnd()  # створення вікна
    window.show()  # відображення вікна
    sys.exit(app.exec_())  # завершення програми



if __name__ == "__main__":  # перевірка чи ми запускаємо головний файл або інклудимо його
    price_open()
    mainWindow_open()  # відкриваємо вікно з прайсом
# downlod_price.py