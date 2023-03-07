import random
import re
import sys
import csv
import os
import requests
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItemModel, QDesktopServices
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QProgressDialog
import datetime

import img_viwer
from Open_Price import open_price
from Price_Window import *
from Search_txt_in_price import find_txt_in_price
from main_Full_Updete_Price import *
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt5.QtGui import QPixmap
import time

# Створення Splash Screen
app_w = QApplication([])
splash = QSplashScreen(QPixmap("./Shablon/start.png"))
splash.show()

# # Створення QProgressDialog
# progress_dialog = QProgressDialog("Loading...", "Cancel", 0, 100, splash)
# progress_dialog.setWindowTitle("Loading...")
# progress_dialog.setWindowModality(Qt.WindowModal)
# progress_dialog.setCancelButton(None)
# progress_dialog.setAutoClose(True)
#
# # Показ QProgressDialog та завантаження ресурсів та ініціалізація програми
# for i in range(101):
#     progress_dialog.setValue(i)
#     app_w.processEvents()
#     time.sleep(0.01) # Реалістично затримка завантаження


class MyForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_img.mouseDoubleClickEvent = self.viwe_img

    indx = 0

    def viwe_img(self, pixmap_all, index):
        index = 0 if index > len(pixmap_all) else index
        global indx
        indx = index
        pixmap = QPixmap(pixmap_all[index])
        img_viwer.Form_viwer = QtWidgets.QWidget()
        ui_viwer = img_viwer.Ui_Form_viwer()
        ui_viwer.setupUi(img_viwer.Form_viwer)
        ui_viwer.label.setPixmap(pixmap)
        img_viwer.Form_viwer.show()
        app.exec_()

    # def keyPressEvent(self, event):
    #     if not event.key() == QtCore.Qt.Key_Space:
    #         # Викликати вашу функцію
    #         # print(event.key)
    #         super().keyPressEvent(event)


ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
]

pixmap_all = []
label_width = 0
label_height = 0
art_old = ''
global me_art
global data
url_s = ['https://viyar.ua/store/Items/photos/ph', '.jpg']


class CustomSortModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left, right):
        if left.column() == right.column() == 2 or left.column() == right.column() == 0:  # Якщо це колонка з ціною (індекс 2)
            if left.data() and right.data():
                left_data = float(left.data())
                right_data = float(right.data())
                return left_data < right_data
            else:
                return False
        else:
            return super().lessThan(left, right)


app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
# -----------Створюємо модель даних і встановлюємо її в treeView-------------------------------------------
ui.model = QtGui.QStandardItemModel()
ui.treeView.setModel(ui.model)
ui.treeView.setAlternatingRowColors(True)  # чергування кольру рядків

ui.model_null = QtGui.QStandardItemModel()
ui.treeView_2.setModel(ui.model_null)
ui.treeView_2.setAlternatingRowColors(True)  # чергування кольру рядків


# -----------вмикаємо підтримку сортування--------------------------------------------------------------------
def me_sort_mod(me_model, obj_view):
    ui.sortModel = CustomSortModel()
    ui.sortModel.setSourceModel(me_model)
    obj_view.setModel(ui.sortModel)
    obj_view.selectionModel().selectionChanged.connect(treeView_selectionChanged)
    obj_view.setSortingEnabled(True)


def interior(me_model, obj_view):
    # -----------Встановлюємо заголовки стовпців---------------------------------------------------------------
    me_model.setHorizontalHeaderLabels(['Артикул', 'Назва виробу', 'Ціна', 'Одиниці', 'Категорія'])
    header = obj_view.header()
    header.resizeSection(0, 80)
    header.resizeSection(1, 400)
    header.resizeSection(2, 60)
    header.resizeSection(3, 60)

    # -----------встановлюємо іконку для заголовка колонки--------------------------------------------------------
    header = obj_view.header()
    header.setSortIndicator(0, QtCore.Qt.AscendingOrder)
    header.setSortIndicator(1, QtCore.Qt.AscendingOrder)
    header.setSortIndicator(2, QtCore.Qt.AscendingOrder)
    header.setSortIndicator(3, QtCore.Qt.AscendingOrder)
    header.setSortIndicator(4, QtCore.Qt.AscendingOrder)


# -----------Заповнюємо модель даних елементами з масиву------------------------------------------------------
def setData(data_rez):
    # print(data_rez)
    clear_model(ui.treeView, ui.model)
    ui.model.invisibleRootItem().clearData()
    for item in data_rez:
        root = ui.model.invisibleRootItem()
        root.appendRow([QtGui.QStandardItem(item['Article']),
                        QtGui.QStandardItem(item['Name']),
                        QtGui.QStandardItem(item['Price']),
                        QtGui.QStandardItem(item['Unit']),
                        QtGui.QStandardItem(item['Category'])])
    ui.treeView.setModel(ui.model)
    ui.retranslateUi(Form)
    QtCore.QMetaObject.connectSlotsByName(Form)
    me_sort_mod(ui.model_null, ui.treeView_2)
    interior(ui.model_null, ui.treeView_2)
    ui.model_null.setHorizontalHeaderLabels(['Артикул', 'Назва виробу', 'Ціна', 'Одиниці', 'Кількість'])
    ui.treeView_2.setModel(ui.model_null)


def clear_model(me_treeview, me_model):
    me_model.removeRows(0, me_model.rowCount())
    me_treeview.setModel(me_model)


# -----------------Метод для обробки clicked на елементі treeView-----------------------------------
def treeView_selectionChanged(selected, deselected):
    global art_old
    index = selected.indexes()[0]
    my_model = index.model()
    row = index.row()
    art = my_model.index(row, 0).data()  # отримуємо артикул
    if art != art_old:
        art_old = art
        update_image(art)


# -----------------функція пошуку по назві-----------------------------------------------------
def find_in():
    global data
    header = ui.treeView.header()
    column = header.sortIndicatorSection()
    order = header.sortIndicatorOrder()
    ui.treeView.setSortingEnabled(False)
    min_price = float(ui.lineEdit_min.text()) if ui.lineEdit_min.text() else 0
    max_price = float(ui.lineEdit_max.text()) if ui.lineEdit_max.text() != '0' else float(10 ** 22)

    data_price = list(filter(lambda x: min_price <= float(x['Price']) <= max_price, data))

    txt = ui.lineEdit_SearchArt.text()
    if len(txt) > 1:
        data_art = find_txt_in_price(txt.lower(), data_price, 'Article')
    else:
        data_art = data_price

    txt = ui.comboBox.currentText()
    if len(txt) > 1:
        data_category = find_txt_in_price(txt.lower(), data_art, 'Category')
    else:
        data_category = data_art

    txt = ui.lineEdit_SearchName.text()
    if len(txt) > 1:
        data_name = find_txt_in_price(txt.lower(), data_category, 'Name')
    else:
        data_name = data_category
    if not len(data_name) == ui.treeView.model().rowCount():
        ui.model2 = QStandardItemModel()
        interior(ui.model2, ui.treeView)
        for item in data_name:
            ui.model2.appendRow([QtGui.QStandardItem(item['Article']),
                                 QtGui.QStandardItem(item['Name']),
                                 QtGui.QStandardItem(item['Price']),
                                 QtGui.QStandardItem(item['Unit']),
                                 QtGui.QStandardItem(item['Category'])])
        # встановити нову модель у treeView
        ui.treeView.setModel(ui.model2)
        row_count = ui.model2.rowCount()
        ui.label.setText(f"Кількість знайдених результатів: {row_count}")
        # вивести модель

        me_sort_mod(ui.treeView.model(), ui.treeView)
        ui.treeView.show()
        ui.treeView.setSortingEnabled(True)
        ui.treeView.sortByColumn(column, order)
        ui.treeView.selectionModel().selectionChanged.connect(treeView_selectionChanged)


# ----------------Метод для обробки подвійного doubleClicked на елементі treeView-----------------
def treeView_doubleClicked(index):
    my_model = index.model()
    """
    Обробляє подвійний клік на записі у treeView1.
    Додає відповідний запис до treeView2.
    """
    # Отримати дані виділеного рядка treeView1
    row_data = [my_model.data(my_model.index(index.row(), column)) for column in range(my_model.columnCount())]
    # print(row_data)
    count_me_dialog, ok_pressed = QInputDialog.getInt(QtWidgets.QWidget(), "Кількість", "Введіть кількість:", value=1)
    if ok_pressed:
        row_data[len(row_data) - 1] = count_me_dialog
        # Додати рядок у treeView2
        add_row_to_treeview(row_data, ui.treeView_2)

    # Оновити вигляд treeView2
    ui.treeView_2.update()


def treeView_del_selection_row(index):
    model = ui.treeView_2.model()
    row = index.row()
    model.removeRow(row)


# ----------------Метод для обробки подвійного Clicked на елементі treeView.Header-----------------
def handleHeaderClick(index):
    me_sort_mod(ui.treeView.model(), ui.treeView)
    # print(f'Header clicked: column {index}')


# ----------------------------------------------------------------------------------------------------------
# ---------------ЗОБРАЖЕННЯ---------------------------------------------------------------------------------


def load_image(url):
    pixmap = QPixmap()
    try:
        response = requests.get(url, headers={'User-Agent': random.choice(ua)})
        pixmap.loadFromData(response.content)
        return pixmap
    except:
        # with open('Shablon/img_not.jpg', "rb") as f:
        #     not_img_file = f.read()
        #     pixmap_not.loadFromData(not_img_file)
        return pixmap


def load_first_image(art):
    url = url_s[0] + art + url_s[1]
    global art_old
    art_old = art
    ui.label_5.setText('https://viyar.ua/ua/search/?q=' + art)
    return load_image(url)


def slider_change():
    global pixmap_all
    get_image(ui.label_img, pixmap_all[ui.horizontalScrollBar.value()])


def count_image(art):
    pixmap = load_first_image(art)
    index = 0
    global pixmap_all
    pixmap_all = []
    while not pixmap.isNull():
        pixmap_all.append(pixmap)
        index += 1
        n = str('_' + str(index + 1))
        next_url = url_s[0] + art + n + url_s[1]
        pixmap = load_image(next_url)
    return index - 1


def get_image(label, pixmap):
    # Отримати оригінальний розмір зображення
    original_width = pixmap.width()
    original_height = pixmap.height()
    global label_width
    global label_height
    # Отримати розміри label
    if label_width == 0 or label_height == 0:
        label_width = label.width()
        label_height = label.height()

    # Обчислити нові розміри зображення зберігаючи пропорцію
    if original_width > label_width or original_height > label_height:
        width_ratio = label_width / original_width
        height_ratio = label_height / original_height
        ratio = min(width_ratio, height_ratio)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        pixmap = pixmap.scaled(new_width, new_height, QtCore.Qt.KeepAspectRatio)
    label.setPixmap(pixmap)


def update_image(art):
    global me_art
    me_art = art
    ui.label_art.setText(me_art)
    get_image(ui.label_img, load_first_image(me_art))
    c = count_image(me_art)
    if c < 0:
        ui.horizontalScrollBar.setMaximum(0)
        with open('Shablon/img_not.jpg', "rb") as f:
            not_img_file = f.read()
            pixmap_not = QPixmap()
            pixmap_not.loadFromData(not_img_file)
        get_image(ui.label_img, pixmap_not)
    else:
        ui.horizontalScrollBar.setMaximum(c)


# ----------------------------------------------------------------------------------------------------------
# ---------------END ЗОБРАЖЕННЯ---------------------------------------------------------------------------------

def add_row_to_treeview(row_data, treeview):
    """
    Додає рядок до заданого дерева вузлів.
    """
    model = treeview.model()
    model.insertRow(model.rowCount())
    for column, value in enumerate(row_data):
        index = model.index(model.rowCount() - 1, column)
        model.setData(index, value)
    treeview.selectionModel().selectionChanged.connect(treeView_selectionChanged)


def update_price(updt=False):
    if updt:
        load_update()
        start()


global art_0
global tmp
global len_data


def start():
    global art_0
    global tmp
    global data
    global len_data
    tmp = []
    file_tmp = open_price()
    data = file_tmp[0]
    len_data = len(data)
    # print(data)
    categories = list(set([d['Category'] for d in data]))
    categories.sort()
    # Додаємо унікальні категорії у комбінований список
    ui.comboBox.addItems(categories)

    # Виводимо комбінований список на екран
    ui.comboBox.show()
    ui.comboBox.setCurrentIndex(-1)

    # ui.treeView = MyTreeView()
    ui.treeView.setSortingEnabled(True)
    interior(ui.model, ui.treeView)
    setData(data)

    r = str(ui.treeView.model().rowCount())
    nm_prise = str(file_tmp[1]).split('.')[-2].split('/')[-1]

    ui.label_PriceDataName.setText(nm_prise)
    ui.label.setText('Кількість знайдених результатів: ' + r)
    art_0 = ui.treeView.model().index(0, 0).data()


# ------------------conext menu-------------------------------------------------
# ------------------------------------------------------------------------------
def showContextMenu(point):
    menu = QtWidgets.QMenu(ui.treeView)
    # додавання пункту меню
    action_add = menu.addAction('Додати до списку замовлення')
    # action2 = menu.addAction('Action 2')
    # показ контекстного меню
    action_add.triggered.connect(on_action_add_triggered)
    # action_add.triggered.connect(lambda: print('1'))
    # action2.triggered.connect(lambda: print('Action 2 triggered'))
    menu.exec_(ui.treeView.mapToGlobal(point))


def showContextMenu_2(point):  # якщо модель порожня, виконуємо певні дії
    menu_2 = QtWidgets.QMenu(ui.treeView_2)
    # додавання пункту меню
    action_kol = menu_2.addAction('Змінити кількість')
    action_del = menu_2.addAction('Відалити зі списку замовлення')
    # показ контекстного меню
    if ui.treeView_2.model().rowCount() > 0:
        action_kol.triggered.connect(on_action_kol_triggered)
        action_del.triggered.connect(on_action_del_triggered)
        # print("Дані присутні")
    else:
        # якщо модель не порожня, виконуємо інші дії
        action_kol.setEnabled(False)
        action_del.setEnabled(False)
        # print("Дані відсутні")
    menu_2.exec_(ui.treeView_2.mapToGlobal(point))


def on_action_add_triggered():
    # print("Action 1 triggered")
    treeView_doubleClicked(ui.treeView.currentIndex())


def on_action_kol_triggered():
    count_me_dialog, ok_pressed = QInputDialog.getInt(QtWidgets.QWidget(), "Кількість", "Введіть кількість:", value=1)
    if ok_pressed:
        model = ui.treeView_2.model()
        row = ui.treeView_2.currentIndex().row()
        column = 4
        itm = model.index(row, column)
        model.setData(itm, count_me_dialog)
        ui.treeView_2.update(itm)


def on_action_del_triggered():
    treeView_del_selection_row(ui.treeView_2.currentIndex())


# --------------------------Save file-----------------------------------------------------------------
def save_to_csv():
    # Відкрити діалогове вікно для вибору шляху до файлу
    if not os.path.isdir('./temp/'):
        os.makedirs('./temp/')
    if ui.treeView_2.model().rowCount() > 0:
        f_name = 'Замовлення фурнітури Віяр від ' + datetime.datetime.now().strftime('%d_%m_%Y')
        file_dialog = QtWidgets.QFileDialog(Form)
        temp_folder = os.path.abspath('./temp/')
        file_dialog.setDirectory(temp_folder)
        path, _ = file_dialog.getSaveFileName(Form, "Save File", os.path.join(temp_folder, f_name), "CSV Files (*.csv)")

        if path:
            # Відкрити файл для запису
            with open('/Shablon/viyar_form_furniture.csv', newline='') as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                sep = str(dialect.delimiter)
            with open(path, "w", newline="") as f:
                writer = csv.writer(f, delimiter=sep)

                # Записати заголовки
                headers = ['Код', 'К-во']
                writer.writerow(headers)

                # Записати дані
                for row in range(ui.model_null.rowCount()):
                    kod = str(ui.model_null.data(ui.model_null.index(row, 0)))
                    kol = str(ui.model_null.data(ui.model_null.index(row, 4)))
                    values = [kod, kol]
                    writer.writerow(values)


def selectAllOnFocus(me_line_edit):
    me_line_edit.selectAll()
    # print(me_line_edit.objectName())


def to_int(me_line_edit):
    try:
        txt = me_line_edit.text()
        me_line_edit.setText(str(int(re.sub("[^0-9]", "", txt))))
    except:
        me_line_edit.setText('0')
    else:
        find_in()


# --------------------Підключення сигналів-------------------------------------------------------------
ui.lineEdit_SearchName.textChanged.connect(find_in)
ui.lineEdit_SearchArt.textChanged.connect(find_in)
ui.lineEdit_min.textChanged.connect(lambda: to_int(ui.lineEdit_min))
ui.lineEdit_max.textChanged.connect(lambda: to_int(ui.lineEdit_max))
ui.comboBox.editTextChanged.connect(find_in)

ui.treeView.customContextMenuRequested.connect(showContextMenu)
ui.treeView.doubleClicked.connect(treeView_doubleClicked)
ui.treeView.selectionModel().selectionChanged.connect(treeView_selectionChanged)
ui.treeView.header().clicked.connect(lambda: me_sort_mod(ui.treeView.model(), ui.treeView))

ui.treeView_2.customContextMenuRequested.connect(showContextMenu_2)
ui.treeView_2.selectionModel().selectionChanged.connect(treeView_selectionChanged)
ui.treeView_2.doubleClicked.connect(treeView_del_selection_row)

ui.pushButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(ui.label_5.text())))
ui.pushButton_Update.clicked.connect(lambda: update_price(True))
ui.pushButton_Clear.clicked.connect(lambda: clear_model(ui.treeView_2, ui.model_null))
ui.pushButton_SaveViyar.clicked.connect(save_to_csv)

ui.label_img.mouseDoubleClickEvent = lambda event: MyForm().viwe_img(pixmap_all, ui.horizontalScrollBar.value())

header = ui.treeView.header()
header.sectionClicked.connect(handleHeaderClick)

if __name__ == "__main__":
    start()
    ui.treeView.selectionModel().selectionChanged.connect(treeView_selectionChanged)
# Закриття Splash Screen
splash.close()
# progress_dialog.close()
# Показ головного вікна програми
Form.show()
update_image(art_0)
ui.horizontalScrollBar.valueChanged.connect(slider_change)

sys.exit(app.exec_())
