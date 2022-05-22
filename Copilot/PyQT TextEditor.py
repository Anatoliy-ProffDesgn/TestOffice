from builtins import print

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog

import sys


class TEditWindow(QMainWindow):  # формуєм наше головне вікно
    def __init__(self):  # викликаємо конструктор батьківського класу
        super(TEditWindow, self).__init__()  # викликаємо конструктор батьківського класу
        self.setWindowTitle("Редактор тексту")  # встановлюємо заголовок вікна
        self.setGeometry(300, 300, 500, 250)  # встановлюємо положення та розміри вікна

        self.textEdit = QtWidgets.QTextEdit(self)  # створюємо текстовий редактор
        self.setCentralWidget(self.textEdit)  # встановлюємо текстовий редактор як віджет головного вікна

        self.createMenuBar()  # створюємо меню

    def createMenuBar(self):  # створюємо меню
        self.menuBar = QMenuBar(self)  # створюємо панель меню
        self.setMenuBar(self.menuBar)  # встановлюємо панель меню як віджет головного вікна

        fileMenu = QMenu("&Файл", self.menuBar)  # створюємо пункт меню "Файл"
        self.menuBar.addMenu(fileMenu)  # додаємо пункт меню "Файл" в панель меню

        newFile = fileMenu.addAction("&Новий", self.click_Actions)  # створюємо пункт меню "Новий"
        openFile = fileMenu.addAction("&Відкрити", self.click_Actions)  # створюємо пункт меню "Відкрити"
        safeFile = fileMenu.addAction("&Зберегти", self.click_Actions)  # створюємо пункт меню "Зберегти"

    @QtCore.pyqtSlot()  # визначаємо слот для пункту меню
    def click_Actions(self):  # визначаємо функцію для пункту меню
        action = self.sender()  # отримуємо посилання на викликаний пункт меню
        try: # спробуємо виконати код нижче (Відлов помилки)
            if action.text() == "&Новий":
                self.textEdit.clear()   # очищуємо текстовий редактор
            elif action.text() == "&Відкрити":
                fName = QFileDialog.getOpenFileName(self, "Відкрити файл", "", "Text files (*.txt)") # відкриваємо файл
                if fName[0]: # перевіряємо чи обрано файл
                    with open(fName[0], 'r') as f:   # відкриваємо файл для читання
                        self.textEdit.setText(f.read()) # встановлюємо текст в текстовий редактор
            elif action.text() == "&Зберегти":
                fName = QFileDialog.getSaveFileName(self, "Зберегти файл", "TextEditorPyQT File", "Text files (*.txt)") # відкриваємо файл
                if fName[0]: # перевіряємо чи обрано файл
                    with open(fName[0], 'w') as f:   # відкриваємо файл для запису
                        f.write(self.textEdit.toPlainText())    # записуємо текст з текстового редактора
        except Exception as e:  # виконуємо вихідний код в разі помилки
            print(e)


def main():  # функція для запуску програми
    app = QApplication(sys.argv)  # передаємо системні параметри в програму
    window = TEditWindow()  # створюємо об'єкт класу TEditWindow
    window.show()  # відображаємо вікно
    sys.exit(app.exec_())  # вихід з програми при натисканні кнопки закриття


if __name__ == '__main__':  # перевірка чи ми запускаємо головний файл
    main()  # запускаємо функцію main()
