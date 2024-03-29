import csv
import datetime
import os
import threading
from tkinter import *
from PIL import Image, ImageTk
import pyperclip
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtCore import QStringListModel, QModelIndex, QUrl, QAbstractTableModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QDesktopServices
from PyQt5.QtWidgets import QInputDialog, QTreeView, QSplashScreen, QStyledItemDelegate, QFileDialog, QDesktopWidget

import Images as img
import img_window as img_w
from CustomPrice import save_custom_price
from Open_Price import open_price, open_custom_price
from Price_Window import Ui_Form
from Search_txt_in_price import find_txt_in_price
from main_Full_Updete_Price import load_update

# -------------------Global-------------------------
global full_model, custom_model, old_model, null_model, save_model
global full_category, custom_category
global label_width, label_height
global pixmaps
global datas
global sorting


class MyTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = self._data[index.row()]
            if index.column() < len(row):
                return row[index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return f"{section + 1}"


class CustomSortModel(QtCore.QSortFilterProxyModel):
    global sorting

    def lessThan(self, left, right):
        # Сортувати як числа колонки (індекс 2 та 0)
        if sorting:
            if left.column() == right.column() == 2 or left.column() == right.column() == 0:
                if left.data() and right.data():
                    left_data = float(left.data())
                    right_data = float(right.data())
                    return left_data < right_data
                else:
                    return False
            else:
                return super().lessThan(left, right)
        else:
            return False


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        pix = QPixmap('images/start.png')
        h = int(pix.height())  # отримаємо висоту вікна і ширину splash
        w = int(pix.width())
        pix = pix.scaled(w, h)  # змінимо розміри зображення
        self.splash = QSplashScreen(pix)
        self.splash.show()
        self.splash.showMessage("ProffДизайн +38(098)926-05-05\n\n\n\n\n...", Qt.AlignBottom | Qt.AlignHCenter, Qt.white)
        self.splash.showMessage("ProffДизайн +38(098)926-05-05\n\n\n\n\nСтворення головного вікна...", Qt.AlignBottom | Qt.AlignHCenter, Qt.white)
        global sorting
        sorting = True

        # Create a bold_font
        bold_font = QtGui.QFont()
        bold_font.setBold(True)

        # Create an instance of the form
        self.ui = Ui_Form()

        # Call the setupUi method passing self as parent
        self.ui.setupUi(self)

        # Create a QStandardItemModel and set it as the model of the treeView
        self.model = QtGui.QStandardItemModel()

        # Create a treeView
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
        self.ui.treeView.header().setSortIndicatorShown(True)
        self.ui.treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.ui.treeView.doubleClicked.connect(self.on_tree_view_double_clicked)
        self.ui.treeView.clicked.connect(self.on_tree_view_clicked)
        self.ui.treeView.setAlternatingRowColors(True)

        # Create a treeView_2
        self.ui.treeView_2.setAlternatingRowColors(True)
        # іelf.ui.treeView_2.model().dataChanged.connect(self.on_data_changed)
        self.ui.treeView_2.clicked.connect(self.on_tree_view_2_clicked)
        self.ui.treeView_2.doubleClicked.connect(self.on_tree_view_double_clicked)

        # Create a context_menu
        self.context_menu = QtWidgets.QMenu(self)
        self.context_menu.addAction(QtGui.QIcon("images/icons/add_96px.png"), "Замовити",
                                    self.add_row_to_treeview_2).setFont(bold_font)
        self.context_menu.addSeparator()
        self.context_menu.addAction(QtGui.QIcon("images/icons/del_96px.png"), "Видалити", self.del_select_row)
        self.context_menu.addSeparator()
        self.context_menu.addAction(QtGui.QIcon("images/icons/full_list_96px.png"), "Повний прайс",
                                    self.full_price_triggered)
        self.context_menu.addAction(QtGui.QIcon("images/icons/me_list_96px.png"), "Мій прайс",
                                    self.custom_price_triggered)
        self.context_menu.addSeparator()
        self.context_menu.addAction(QtGui.QIcon("images/icons/save_as_96px.png"), "Замінити мій прайс",
                                    self.custom_price_resave)
        self.context_menu.addAction(QtGui.QIcon("images/icons/save_96px.png"), "Додати у мій прайс",
                                    self.custom_price_save)
        self.context_menu.addSeparator()
        self.context_menu.addAction(QtGui.QIcon("images/icons/update_96px.png"), "Оновити прайс",
                                    lambda: self.update_price(True))
        # self.context_menu.addAction("Оновити прайс", partial(self.update_price, True))
        self.ui.treeView.customContextMenuRequested.connect(self.show_context_menu)

        # Create a context_menu_2
        self.context_menu_2 = QtWidgets.QMenu(self)
        self.context_menu_2.addAction(QtGui.QIcon("images/icons/to_add_96px.png"), "Змінити кількість",
                                      self.on_action_kol_triggered).setFont(bold_font)
        self.context_menu_2.addSeparator()
        self.context_menu_2.addAction(QtGui.QIcon("images/icons/del_96px.png"), "Видалити", self.del2_select_row)
        self.context_menu_2.addAction(QtGui.QIcon("images/icons/clear_96px.png"), "Очистити все", self.del_all_row)
        self.context_menu_2.addSeparator()
        self.context_menu_2.addAction(QtGui.QIcon("images/icons/save_as_96px.png"), "Замінити мій прайс",
                                      self.custom_price2_resave)
        self.context_menu_2.addAction(QtGui.QIcon("images/icons/save_96px.png"), "Додати у мій прайс",
                                      self.custom_price2_save)
        self.context_menu_2.addSeparator()
        self.context_menu_2.addAction(QtGui.QIcon("images/icons/export_csv_96px.png"), "Завантажити .csv",
                                      self.open_csv)
        self.context_menu_2.addAction(QtGui.QIcon("images/icons/save_csv_96px.png"), "Зберегти для Віяру *.csv",
                                      self.save_to_csv).setFont(bold_font)
        self.ui.treeView_2.customContextMenuRequested.connect(self.show_context_menu_2)

        # Create a lineEdit-s
        self.ui.lineEdit_SearchName.textEdited.connect(self.find_in)
        self.ui.lineEdit_SearchArt.textEdited.connect(self.find_in)
        self.ui.lineEdit_min.textEdited.connect(self.find_in)
        self.ui.lineEdit_max.textEdited.connect(self.find_in)
        self.ui.comboBox.editTextChanged.connect(self.find_in)

        # Create a pushButton-s
        self.ui.pushButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self.ui.pushButton.text())))
        self.ui.pushButton_Past.clicked.connect(self.paste_clipboard)

        # -------------------Global-------------------------
        global datas
        global full_model, custom_model, null_model
        global full_category, custom_category

        # -------------------мій функціонал-------------------------

        self.img_window = None  # define img_window as an instance variable
        me_data = open_price()
        price_name = me_data[1][0]
        price_name = price_name.split('/')[-1].split('.')[0]
        self.setWindowTitle('ProffДизайн  |  +38(098)926-05-05  |  ' + price_name)
        full_model = self.create_me_model(me_data[0])
        full_category = self.create_category(me_data[0])
        null_model = self.create_me_model([])
        self.treeView_set_model(self.ui.treeView_2, null_model)
        null_model.horizontalHeaderItem(null_model.columnCount() - 1).setText('Кількість')
        null_model.horizontalHeaderItem(null_model.columnCount() - 2).setText('Сума')
        datas = me_data[0]
        self.treeView_set_model(self.ui.treeView, full_model)
        self.combo_box_set_data()
        self.ui.label.setText('Знайдено: ' + str(self.ui.treeView.model().rowCount()))
        self.ui.treeView_2.model().dataChanged.connect(self.on_treeView_2_Changed)
        self.ui.treeView_2.model().rowsInserted.connect(self.on_treeView_2_Changed)  # додайте цей рядок
        self.ui.treeView_2.model().rowsRemoved.connect(self.on_treeView_2_Changed)


    def paste_clipboard(self):
        data = pyperclip.paste()
        # перевірка наявності данних у self._data якщо self.data == '' або data == \\r\\n то вважаєм що данних нема
        if data == '' or data == '\r\n':
            data = 'У буфері обміну відсутні данні\r\nСкопіюйте таблицю яку хочете тут розмістити'
        rows = data.split('\r\n')
        rows = [row.split('\t') for row in rows]
        model = MyTableModel(rows)
        view = self.ui.treeView_3
        view.setModel(model)
        # view to check style sheet
        # Встановлюємо делегат для дерева QTreeView
        view.setItemDelegateForColumn(0, QStyledItemDelegate(view))
        # Встановлюємо стиль для дерева QTreeView
        view.setStyleSheet('''
            QTreeView::indicator:checked {
                image: url(images/check.png);
            }
        ''')
        view.setSelectionMode(QTreeView.MultiSelection)
        view.setEditTriggers(QTreeView.DoubleClicked)
        view.setColumnWidth(0, 260)
        view.setColumnWidth(1, 30)
        view.setColumnWidth(2, 20)
        view.setColumnWidth(4, 20)
        view.show()

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

    def on_tree_view_clicked(self, index: QModelIndex):
        art = self.ui.treeView.model().index(index.row(), 0).data()
        self.ui.pushButton.setText('https://viyar.ua/ua/search/?q=' + art)

    def on_tree_view_2_clicked(self, index: QModelIndex):
        art = self.ui.treeView_2.model().index(index.row(), 0).data()
        self.ui.pushButton.setText('https://viyar.ua/ua/search/?q=' + art)
        model = self.ui.treeView.model()  # Пройтися по всіх елементах моделі
        for row in range(model.rowCount()):
            index = model.index(row, 0)  # Отримати індекс елемента за допомогою моделі
            data = model.data(index)  # Отримати дані елемента за допомогою індексу
            if data == art:  # Порівняти дані зі шуканим значенням
                row_index = model.index(row, 0)  # Отримати індекс рядка
                self.ui.treeView.selectionModel().select(row_index,
                                                         QtCore.QItemSelectionModel.ClearAndSelect)  # Виділити рядок
                self.ui.treeView.scrollTo(row_index, QtWidgets.QAbstractItemView.EnsureVisible)
                break

    def on_tree_view_double_clicked(self, index: QModelIndex):
        print(f"Подвійний клік на елементі з індексом {index.row()}")
        art = index.model().index(index.row(), 0).data()
        name = index.model().index(index.row(), 1).data()
        self.update_image(art, name)

    def create_category(self, me_data):
        category = list(set([d['Category'] for d in me_data]))
        category.sort()
        return category

    def create_me_model(self, me_data):
        # Створення моделі
        self.splash.showMessage("ProffДизайн +38(098)926-05-05\n\n\n\n\nСтворення моделі...", Qt.AlignBottom | Qt.AlignHCenter, Qt.white)
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
        self.splash.showMessage("ProffДизайн +38(098)926-05-05\n\n\n\n\nНаповнення моделі...", Qt.AlignBottom | Qt.AlignHCenter, Qt.white)
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

    def combo_box_set_data(self, data=None):
        if data is None:
            data = full_category
        model = QStringListModel()
        model.setStringList(data)
        # Додаємо список до комбінованого списку
        self.ui.comboBox.setModel(model)
        self.ui.comboBox.show()
        self.ui.comboBox.setCurrentIndex(-1)

    def show_context_menu(self, point):
        # Show the context menu at the cursor's position
        self.context_menu.exec_(self.ui.treeView.mapToGlobal(point))

    def show_context_menu_2(self, point):
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
                kol = int(count_me_dialog)
                price = float(row_data[-3].text())
                rez = round(kol * price, 2)
                row_data[-1] = QStandardItem(
                    str(kol))  # заміна значення останнього стовпця на введену кількість
                row_data[-2] = QStandardItem(str(rez))
                global null_model  # отримання глобальної змінної null_model
                parent_item = null_model.invisibleRootItem()  # отримання кореневого елемента дерева
                parent_item.appendRow(row_data)  # додавання нового рядка до дерева

    def dublicate_remove(self):
        model = self.ui.treeView_2.model()
        for row in range(model.rowCount()):
            item = model.index(row, 0)
            kol_item=model.index(row, model.columnCount() - 1)
             # ззворотнім перебором починаючи з останнього елемента у treeView_2.model() знаходим дублікати в моделі й видаляємо їх
            for i in range(row + 1, model.rowCount()):
                item_2 = model.index(i, 0)
                if item.data() == item_2.data():
                    kol1 = int(model.data(model.index(row, model.columnCount() - 1)))
                    kol2 = int(model.data(model.index(i, model.columnCount() - 1)))
                    sum=str(kol1+kol2)
                    tmp=kol_item.data()
                    model.removeRow(i)
                    model.setData(kol_item, sum)
                    self.ui.treeView_2.update()

    # update_summ def


    def on_treeView_2_Changed(self):
        self.dublicate_remove()
        try:
            model = self.ui.treeView_2.model()
            column = model.columnCount() - 2  # get the second last column
            sum = 0
            for row in range(model.rowCount()):
                index = model.index(row, column)
                value = model.data(index)
                sum += float(value)
            print(sum)  # print the sum of the column
            self.ui.label_summ.setText('Сума: ' + str(round(sum, 2)))
        except:
            self.ui.label_summ.setText('Сума:______')


    def del_select_row(self):
        selection_model = self.ui.treeView.selectionModel()  # Отримати вибрану модель виділень
        selected_rows = selection_model.selectedRows()  # Отримати список виділених рядків
        for row in reversed(selected_rows):  # Видалити виділені рядки з моделі
            self.ui.treeView.model().removeRow(row.row())
        self.label_count()

    def del2_select_row(self):
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
        global datas
        me_custom_data = open_custom_price()
        custom_model = self.create_me_model(me_custom_data)
        custom_category = self.create_category(me_custom_data)
        datas = self.model_to_dict(custom_model)
        self.treeView_set_model(self.ui.treeView, custom_model)
        self.combo_box_set_data(custom_category)
        self.ui.label.setText('Знайдено: ' + str(self.ui.treeView.model().rowCount()))

    def on_action_kol_triggered(self):
        global sorting
        model = self.ui.treeView_2.model()
        row = self.ui.treeView_2.currentIndex().row()
        kol = model.data(model.index(row, 4))
        if kol is None:
            return

        count_me_dialog, ok_pressed = QInputDialog.getInt(
            QtWidgets.QWidget(), "Кількість", "Введіть кількість:", value=int(kol))
        if ok_pressed:
            sorting = False
            model.setData(model.index(row, 4), count_me_dialog)
            kol = int(count_me_dialog)
            price = float(model.data(model.index(row, 2)))
            rez = round(kol * price, 2)
            model.setData(model.index(row, 3), rez)
            self.ui.treeView_2.update()
            sorting = True

    def custom_price_save(self):
        global datas
        save_custom_price(datas, self.ui.treeView)

    def custom_price_resave(self):
        global datas
        save_custom_price(datas, self.ui.treeView, True)

    def custom_price2_save(self):
        global datas
        save_custom_price(datas, self.ui.treeView_2)

    def custom_price2_resave(self):
        global datas
        save_custom_price(datas, self.ui.treeView_2, True)

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
        # min_price = float(self.ui.lineEdit_min.text()) if self.ui.lineEdit_min.text() else 0
        # max_price = float(self.ui.lineEdit_max.text()) if self.ui.lineEdit_max.text() != '0' else float(10 ** 22)
        try:
            min_price = float(self.ui.lineEdit_min.text())
        except:
            self.ui.lineEdit_min.setText('0')
            min_price = float(0)
        try:
            max_price = float(self.ui.lineEdit_max.text())
            if max_price == 0:
                max_price = float(10 ** 22)
        except:
            self.ui.lineEdit_max.setText('0')
            max_price = float(10 ** 22)
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

    def open_csv(self):
        global datas
        # відкриємо файл за допомогою діалога з запитом на файл .csv за вказаним розміщенням /temp/
        fname = QFileDialog.getOpenFileName(self, 'Open file', './temp/', "CSV files (*.csv)")
        if fname[0]:
            with open(fname[0], 'r') as f:
                reader = csv.reader(f)
                data = list(reader)
            new_data = []
            for item in data:
                art = item[0].split(';')
                # datas = ... [{'Article': '83093', 'Name': 'Полиця для паперу одинарна хром', 'Price': '300.42', 'Unit': 'грн/шт', 'Category': 'Релінги і комплектуючі'}, ...]
                #  збережем в new_data рядкі  з datas якшо article == art
                for row in datas:
                    if row['Article'] == art[0]:
                        data_tmp = row
                        if data_tmp:
                            data_tmp['Category'] = art[1]
                            data_tmp['Unit'] = float(data_tmp['Price']) * float(data_tmp['Category'])
                            new_data.append(data_tmp)
                            break
            model2 = null_model
            for row in new_data:
                r = []
                r.append(QStandardItem(str(row['Article'])))
                r.append(QStandardItem(str(row['Name'])))
                r.append(QStandardItem(str(row['Price'])))
                r.append(QStandardItem(str(row['Unit'])))
                r.append(QStandardItem(str(row['Category'])))
                model2.appendRow(r)
            self.ui.treeView_2.setModel(model2)
            self.ui.treeView_2.update()
            self.ui.treeView_2.model().dataChanged.connect(self.on_treeView_2_Changed)
            self.ui.treeView_2.model().rowsInserted.connect(self.on_treeView_2_Changed)  # додайте цей рядок
            self.ui.treeView_2.model().rowsRemoved.connect(self.on_treeView_2_Changed)

    def save_to_csv(self):
        # Відкрити діалогове вікно для вибору шляху до файлу
        try:
            if not os.path.isdir('./temp/'):
                os.makedirs('./temp/')
            if self.ui.treeView_2.model().rowCount() > 0:
                f_name = 'Замовлення фурнітури Віяр від ' + datetime.datetime.now().strftime('%d_%m_%Y')
                form = QtWidgets.QWidget()
                file_dialog = QtWidgets.QFileDialog(form)
                temp_folder = os.path.abspath('./temp/')
                file_dialog.setDirectory(temp_folder)
                path, _ = file_dialog.getSaveFileName(form, "Save File", os.path.join(temp_folder, f_name),
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
                        model = self.ui.treeView_2.model()
                        # Записати дані
                        for row in range(model.rowCount()):
                            kod = str(model.data(model.index(row, 0)))
                            kol = str(model.data(model.index(row, 4)))
                            values = [kod, kol]
                            writer.writerow(values)
        except:
            print('Save error')

    def update_price(self, updt=False):
        if updt:
            # Запуск вікна та виконання процесів
            model = QStandardItemModel()
            item1 = QStandardItem('Оновлення прайсу')
            model.appendRow(item1)
            self.ui.treeView_3.setModel(model)
            self.ui.treeView_3.show()
            p = create_window(self.ui.treeView_3)
            p.destroy()
            # p1 = threading.Thread(target=load_update(self.ui.treeView_3))
            # p1.start()
            # p.start()
            # load_update(view=self.ui.treeView_3)
            # p1.join()
            # p.join()


def create_window(view):
    root = Tk()
    # Завантаження анімаційного файлу
    image = Image.open('images/load.gif')
    photo = ImageTk.PhotoImage(image)
    # Створення вікна та додавання до нього анімаційного файлу
    label = Label(root, image=photo, background='gray')
    label.pack()
    label2 = Label(root, text='Оновлення прайсу.\n(може тривати декілька хвилин)',
                   foreground='white',
                   background='gray',
                   font=(None, 8, 'bold'))
    label2.pack()
    root.configure(background='gray')
    # Визначаємо розміри вікна та його розміщення в центрі екрану
    root.geometry("+{}+{}".format(int(root.winfo_screenwidth() / 2 - root.winfo_reqwidth() / 2),
                                  int(root.winfo_screenheight() / 2 - root.winfo_reqheight() / 2)))
    # Встановлюємо передній план для вікна
    root.lift()
    root.wm_attributes('-topmost', 1)
    # root.mainloop()
    root.overrideredirect(True)
    root.update()
    update_image(label, photo)
    load_update(view)
    return root


def update_image(label, image):
    # Запустити gif анімацію
    label.after(100, update_image, label, image)
    label.config(image=image)
    label.image = image
    # label.after(100, update_image)



app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
window.splash.close()
app.exec_()
