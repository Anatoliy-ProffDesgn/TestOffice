import csv
import datetime
import os
import sys
from multiprocessing import Process

from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtCore import QStringListModel, QModelIndex, QUrl, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QMovie, QDesktopServices
from PyQt5.QtWidgets import QHeaderView, QInputDialog, QTreeView, QToolTip, QApplication

import inet_test
from Price_Window import Ui_Form
from Open_Price import open_price
import Images as img
import img_window as img_w
from Search_txt_in_price import find_txt_in_price

# -------------------Global-------------------------
global full_model, custom_model, old_model, null_model, save_model
global full_category, custom_category
global label_width, label_height
global pixmaps
global datas


class CustomSortModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left, right):
        # Сортувати як числа колонки (індекс 2 та 0)
        if left.column() == right.column() == 2 or left.column() == right.column() == 0:
            if left.data() and right.data():
                left_data = float(left.data())
                right_data = float(right.data())
                return left_data < right_data
            else:
                return False
        else:
            return super().lessThan(left, right)


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create an instance of the form
        self.ui = Ui_Form()

        # Call the setupUi method passing self as parent
        self.ui.setupUi(self)

        # Do other stuff here
        # Create a QStandardItemModel and set it as the model of the treeView
        self.model = QtGui.QStandardItemModel()
        self.ui.treeView.setModel(self.model)

        # Sort the data by the first column
        self.ui.treeView.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
        self.ui.treeView.header().setSortIndicatorShown(True)
        self.ui.treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)

        # Connect the context menu signal to a slot
        self.ui.treeView.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.treeView.doubleClicked.connect(self.on_tree_view_double_clicked)
        self.ui.treeView.clicked.connect(self.on_tree_view_clicked)
        self.ui.treeView.setAlternatingRowColors(True)
        self.ui.treeView_2.customContextMenuRequested.connect(self.show_context_menu_2)
        self.ui.treeView_2.setAlternatingRowColors(True)
        self.ui.treeView_2.doubleClicked.connect(self.on_tree_view_double_clicked)

        self.ui.horizontalScrollBar.valueChanged.connect(self.slider_move)

        self.ui.lineEdit_SearchName.textEdited.connect(self.find_in)
        self.ui.lineEdit_SearchArt.textEdited.connect(self.find_in)
        self.ui.lineEdit_min.textEdited.connect(self.find_in)
        self.ui.lineEdit_max.textEdited.connect(self.find_in)
        self.ui.comboBox.editTextChanged.connect(self.find_in)

        # self.ui.pushButton.clicked(lambda: QDesktopServices.openUrl(QUrl(self.ui.label_5.text())))
        # self.ui.pushButton.clicked(lambda: QDesktopServices.openUrl(QUrl(self.ui.label_5.text())))
        self.ui.pushButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self.ui.label_5.text())))
        self.ui.pushButton_SaveViyar.clicked.connect(self.save_to_csv)
        self.ui.pushButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self.ui.pushButton.text())))
        # додатковий код для заповнення treeView
        # ...

        # -------------------Global-------------------------
        global full_model, custom_model, null_model
        global full_category, custom_category
        global datas

        # -------------------мій функціонал-------------------------

        self.img_window = None  # define img_window as an instance variable
        me_data = open_price()
        full_model = self.create_me_model(me_data[0])
        custom_model = self.create_me_model(me_data[2])
        full_category = self.create_category(me_data[0])
        custom_category = self.create_category(me_data[2])
        null_model = self.create_me_model([])
        self.treeView_set_model(self.ui.treeView_2, null_model)
        null_model.horizontalHeaderItem(null_model.columnCount() - 1).setText('Кількість')
        datas = me_data[0]
        self.treeView_set_model(self.ui.treeView, full_model)
        self.combo_box_set_data()
        self.ui.label.setText('Знайдено: ' + str(self.ui.treeView.model().rowCount()))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.ui.treeView.resizeEvent(event)

    def label_count(self):
        self.ui.label.setText('Знайдено: ' + str(self.ui.treeView.model().rowCount()))

    def update_image(self, art, name='Мої зображення'):
        global pixmaps
        pixmaps = img.count_image(art)
        if self.img_window:  # якщо вікно вже існує, закриваємо його
            self.img_window.reject()
        self.img_window = img_w.MyImageDialog(pixmaps, name)
        self.img_window.setModal(True)
        self.img_window.exec_()


        # count = len(pixmaps)
        # img.get_image(self.ui.label_img, pixmaps[0])
        # self.ui.horizontalScrollBar.setMaximum(len(pixmaps) - 1)
        # self.ui.horizontalScrollBar.setValue(0)
        # self.ui.label_art.setText('Доступно ' + str(count) + ' зображень.')


    def on_tree_view_clicked(self, index: QModelIndex):
        art = self.ui.treeView.model().index(index.row(), 0).data()
        # self.ui.label_5.setText('https://viyar.ua/ua/search/?q=' + art)
        self.ui.pushButton.setText('https://viyar.ua/ua/search/?q=' + art)

    def on_tree_view_double_clicked(self, index: QModelIndex):
        print(f"Подвійний клік на елементі з індексом {index.row()}")
        art = index.model().index(index.row(), 0).data()
        name = index.model().index(index.row(), 1).data()
        self.update_image(art, name)

    def slider_move(self):
        global pixmaps
        try:
            index = self.ui.horizontalScrollBar.value()
            count = len(pixmaps)
            img.get_image(self.ui.label_img, pixmaps[self.ui.horizontalScrollBar.value()])
            self.ui.label_art.setText(index + 1, 'із', count, 'зображень.')
        except:
            pass

    def create_category(self, me_data):
        category = list(set([d['Category'] for d in me_data]))
        category.sort()
        return category

    def create_me_model(self, me_data):
        # Створення моделі
        me_model = QStandardItemModel()
        # Встановлення заголовків стовпців
        keys = ['Article', 'Name', 'Price', 'Unit', 'Category']
        header = ['Артикул', 'Назва', 'Ціна', 'Одиниці', 'Категорія']
        me_model.setHorizontalHeaderLabels(header)

        # Додавання даних до моделі
        for data in me_data:
            row = []
            for key in keys:
                item = QStandardItem(str(data.get(key, '')))
                row.append(item)
            me_model.appendRow(row)
        return me_model

    def treeView_set_model(self, tree_view, me_model):
        # -----------Встановлюємо заголовки стовпців---------------------------------------------------------------
        tree_view.setModel(me_model)
        header = tree_view.header()
        header.resizeSection(0, 80)
        header.resizeSection(1, 400)
        header.resizeSection(2, 60)
        header.resizeSection(3, 60)
        # -----------встановлюємо іконку для заголовка колонки-----------------------------------------------------
        header.setSortIndicator(0, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(1, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(2, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(3, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(4, QtCore.Qt.AscendingOrder)

        sort_model = CustomSortModel()
        sort_model.setSourceModel(me_model)
        tree_view.setModel(sort_model)
        tree_view.setSortingEnabled(True)

    def combo_box_set_data(self, data=''):
        if data == '':
            data = full_category
        model = QStringListModel()
        model.setStringList(data)
        # Додаємо список до комбінованого списку
        self.ui.comboBox.setModel(model)
        self.ui.comboBox.show()
        self.ui.comboBox.setCurrentIndex(-1)

    def show_context_menu(self, point):
        # Create a context menu
        self.context_menu = QtWidgets.QMenu(self)
        self.context_menu.addAction("Додати у замовлення", self.add_row_to_treeview_2)
        self.context_menu.addSeparator()
        self.context_menu.addAction("Повний прайс", self.full_price_triggered)
        self.context_menu.addAction("Мій прайс", self.custom_price_triggered)
        # Show the context menu at the cursor's position
        self.context_menu.exec_(self.ui.treeView.mapToGlobal(point))

    def show_context_menu_2(self, point):
        # Create a context menu
        self.context_menu_2 = QtWidgets.QMenu(self)
        self.context_menu_2.addAction("Змінити кількість", self.full_price_triggered)
        self.context_menu_2.addSeparator()
        self.context_menu_2.addAction("Видалити рядок", self.del_select_row)
        self.context_menu_2.addAction("Очистити все", self.del_all_row)
        # Show the context menu at the cursor's position
        self.context_menu_2.exec_(self.ui.treeView_2.mapToGlobal(point))

    def add_row_to_treeview_2(self):
        selected_indexes = self.ui.treeView.selectionModel().selectedIndexes()  # отримання списку індексів виділених рядків
        if len(selected_indexes) > 0:  # перевірка, чи є хоча б один виділений рядок
            selected_indexes = self.ui.treeView.selectionModel().selectedIndexes()  # отримання списку індексів виділених рядків
            model = self.ui.treeView.model()  # отримання моделі дерева
            row_data = [
                QStandardItem(model.data(index)) for index in
                selected_indexes]  # створення списку з елементів виділених рядків
            count_me_dialog, ok_pressed = QInputDialog.getInt(
                QtWidgets.QWidget(), "Кількість", "Введіть кількість:",
                value=1)  # створення діалогового вікна для введення кількості
            if ok_pressed:  # перевірка, чи було натиснуто кнопку "ОК" у діалоговому вікні
                row_data[-1] = QStandardItem(
                    str(count_me_dialog))  # заміна значення останнього стовпця на введену кількість
                global null_model  # отримання глобальної змінної null_model
                parent_item = null_model.invisibleRootItem()  # отримання кореневого елемента дерева
                parent_item.appendRow(row_data)  # додавання нового рядка до дерева

    def del_select_row(self):
        selection_model = self.ui.treeView_2.selectionModel()  # Отримати вибрану модель виділень
        selected_rows = selection_model.selectedRows()  # Отримати список виділених рядків
        for row in reversed(selected_rows):  # Видалити виділені рядки з моделі
            self.ui.treeView_2.model().removeRow(row.row())

    def del_all_row(self):
        for row in reversed(range(self.ui.treeView_2.model().rowCount())):  # Видалити виділені рядки з моделі
            self.ui.treeView_2.model().removeRow(row)

    def full_price_triggered(self):
        # Handle Повний прайс
        global datas
        datas = self.model_to_dict(full_model)
        self.treeView_set_model(self.ui.treeView, full_model)
        self.combo_box_set_data()
        self.ui.label.setText('Знайдено: ' + str(self.ui.treeView.model().rowCount()))
        # print("Action 1 triggered")

    def custom_price_triggered(self):
        # Handle action 2
        global datas
        datas = self.model_to_dict(custom_model)
        self.treeView_set_model(self.ui.treeView, custom_model)
        self.combo_box_set_data(custom_category)
        self.ui.label.setText('Знайдено: ' + str(self.ui.treeView.model().rowCount()))
        # print("Action 2 triggered")

    def model_to_dict(self, me_model):
        data = []
        key = ['Article', 'Name', 'Price', 'Unit', 'Category']
        for row in range(me_model.rowCount()):
            row_data = {}
            for column in range(me_model.columnCount()):
                index = me_model.index(row, column)
                row_data[key[column]] = me_model.data(index)
            data.append(row_data)
        return data

    def find_in(self):
        global datas
        header = self.ui.treeView.header()
        column = header.sortIndicatorSection()
        order = header.sortIndicatorOrder()
        self.ui.treeView.setSortingEnabled(False)
        min_price = float(self.ui.lineEdit_min.text()) if self.ui.lineEdit_min.text() else 0
        max_price = float(self.ui.lineEdit_max.text()) if self.ui.lineEdit_max.text() != '0' else float(10 ** 22)
        data_price = list(filter(lambda x: min_price <= float(x['Price']) <= max_price, datas))
        txt = self.ui.lineEdit_SearchArt.text()
        if len(txt) > 1:
            data_art = find_txt_in_price(txt.lower(), data_price, 'Article')
        else:
            data_art = data_price

        txt = self.ui.comboBox.currentText()
        if len(txt) > 1:
            data_category = find_txt_in_price(txt.lower(), data_art, 'Category')
        else:
            data_category = data_art

        txt = self.ui.lineEdit_SearchName.text()
        if len(txt) > 1:
            data_name = find_txt_in_price(txt.lower(), data_category, 'Name')
        else:
            data_name = data_category

        if not len(data_name) == self.ui.treeView.model().rowCount():
            self.ui.model2 = QStandardItemModel()
            self.ui.model2 = self.create_me_model(data_name)
            self.treeView_set_model(self.ui.treeView, self.ui.model2)
            row_count = self.ui.model2.rowCount()
            self.ui.label.setText(f"Знайдено: {row_count}")

            # вивести модель
            self.ui.treeView.show()
            self.ui.treeView.setSortingEnabled(True)
            self.ui.treeView.sortByColumn(column, order)

    def save_to_csv(self):
        # Відкрити діалогове вікно для вибору шляху до файлу
        try:
            if not os.path.isdir('./temp/'):
                os.makedirs('./temp/')
            if self.ui.treeView_2.model().rowCount() > 0:
                f_name = 'Замовлення фурнітури Віяр від ' + datetime.datetime.now().strftime('%d_%m_%Y')
                Form = QtWidgets.QWidget()
                file_dialog = QtWidgets.QFileDialog(Form)
                temp_folder = os.path.abspath('./temp/')
                file_dialog.setDirectory(temp_folder)
                path, _ = file_dialog.getSaveFileName(Form, "Save File", os.path.join(temp_folder, f_name),
                                                      "CSV Files (*.csv)")

                if path:
                    # Відкрити файл для запису
                    with open('Shablon/viyar_form_furniture.csv', newline='') as csvfile:
                        dialect = csv.Sniffer().sniff(csvfile.read(1024))
                        sep = str(dialect.delimiter)
                    with open(path, "w", newline="") as f:
                        writer = csv.writer(f, delimiter=sep)

                        # Записати заголовки
                        headers = ['Код', 'К-во']
                        writer.writerow(headers)
                        model=self.ui.treeView_2.model()
                        # Записати дані
                        for row in range(model.rowCount()):
                            kod = str(model.data(model.index(row, 0)))
                            kol = str(model.data(model.index(row, 4)))
                            values = [kod, kol]
                            writer.writerow(values)
        except:
            print('Save error')


# Create the application and show the main window
app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
app.exec_()
