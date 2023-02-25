from Price_Window import *
from Open_Price import open_price
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QPixmap
from Search_txt_in_price import find_txt_in_price
import requests
import sys
import random

ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
]
user_agent = random.choice(ua)
print(user_agent)
global pixmap_all


class CustomSortModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left, right):
        if left.column() == right.column() == 2 or left.column() == right.column() == 0:  # Якщо це колонка з ціною (індекс 2)
            left_data = float(left.data())
            right_data = float(right.data())
            return left_data < right_data
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


# -----------вмикаємо підтримку сортування--------------------------------------------------------------------
def me_sort_mod(me_model):
    ui.sortModel = CustomSortModel()
    ui.sortModel.setSourceModel(me_model)
    ui.treeView.setModel(ui.sortModel)
    ui.treeView.setSortingEnabled(True)


# -----------встановлюємо індекс колонки, по якій будуть сортуватися дані-------------------------------------
# ui.treeView.setSortingColumn(0)

def interior(me_model):
    # -----------Встановлюємо заголовки стовпців---------------------------------------------------------------
    me_model.setHorizontalHeaderLabels(['Артикул', 'Назва виробу', 'Ціна', 'Одиниці', 'Категорія'])
    header = ui.treeView.header()
    header.resizeSection(0, 80)
    header.resizeSection(1, 400)
    header.resizeSection(2, 60)
    header.resizeSection(3, 60)

    # -----------встановлюємо іконку для заголовка колонки--------------------------------------------------------
    header = ui.treeView.header()
    header.setSortIndicator(0, QtCore.Qt.AscendingOrder)
    header.setSortIndicator(1, QtCore.Qt.AscendingOrder)
    header.setSortIndicator(2, QtCore.Qt.AscendingOrder)
    header.setSortIndicator(3, QtCore.Qt.AscendingOrder)
    header.setSortIndicator(4, QtCore.Qt.AscendingOrder)


# -----------Заповнюємо модель даних елементами з масиву------------------------------------------------------
def setData(data_rez):
    interior(ui.model)
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
    # me_sort_mod(ui.model)
    ui.treeView.setSortingEnabled(True)


# -----------------функція пошуку по назві-----------------------------------------------------
def find_in():
    txt = ui.lineEdit_SearchArt.text()
    if len(txt) > 0:
        data_0 = find_txt_in_price(txt, data, 'Article')
    else:
        data_0 = data
    txt = ui.lineEdit_SearchName.text()
    if len(txt) > 0:
        data_1 = find_txt_in_price(txt, data_0, 'Name')
    else:
        data_1 = data_0
    txt = ui.lineEdit_SearchCategori.text()
    if len(txt) > 0:
        data_2 = find_txt_in_price(txt, data_1, 'Category')
    else:
        data_2 = data_1

    if len(data_2) != len_dada or len(txt) != 0:
        ui.model2 = QStandardItemModel()
        interior(ui.model2)
        for item in data_2:
            ui.model2.appendRow([QtGui.QStandardItem(item['Article']),
                                 QtGui.QStandardItem(item['Name']),
                                 QtGui.QStandardItem(item['Price']),
                                 QtGui.QStandardItem(item['Unit']),
                                 QtGui.QStandardItem(item['Category'])])
        # встановити нову модель у treeView
        ui.treeView.setModel(ui.model2)
        row_count = ui.model2.rowCount()
        ui.label.setText(f"Кількість знайдених результатів: {row_count}")
        # відобразити модель
        ui.treeView.show()


# -----------------Метод для обробки clicked на елементі treeView-----------------------------------
def treeView_clicked(index):
    my_model = index.model()
    row = index.row()
    art = my_model.index(row, 0).data()  # отримуємо артикул
    update_image(art)


# ----------------Метод для обробки подвійного doubleClicked на елементі treeView-----------------
def treeView_doubleClicked(index):
    my_model = index.model()
    row = index.row()
    art = my_model.index(row, 0).data()  # отримуємо артикул
    print(art)


# ----------------Метод для обробки подвійного Clicked на елементі treeView.Header-----------------
def handleHeaderClick(index):
    print(f'Header clicked: column {index}')
    me_sort_mod(ui.treeView.model())


# ----------------Метод для обробки подвійного doubleClicked на елементі treeView.Header-----------------
def handleHeaderDoubleClick(index):
    print(f'Header double clicked: column {index}')


# ----------------------------------------------------------------------------------------------------------
# ---------------ЗОБРАЖЕННЯ---------------------------------------------------------------------------------

url_s = ['https://viyar.ua/store/Items/photos/ph', '.jpg']

global me_art


def load_image(url):
    response = requests.get(url, headers={'User-Agent': random.choice(ua)})
    pixmap = QPixmap()
    pixmap.loadFromData(response.content)
    return pixmap


def load_first_image(art):
    url = url_s[0] + art + url_s[1]
    return load_image(url)


def next_image(old_url, art):
    index = ui.horizontalScrollBar.value()
    if index == 0:
        n = ''
    else:
        n = str('_' + str(index + 1))
    next_url = old_url[0] + art + n + old_url[1]
    return load_image(next_url)


def slider_change():
    pixmap = next_image(url_s, me_art)
    # print(type(pixmap_all(ui.horizontalScrollBar.value())))
    # get_image(ui.label_img, pixmap_all[ui.horizontalScrollBar.value()])
    get_image(ui.label_img, pixmap)


def count_image(art):
    pixmap = load_first_image(art)
    index = 0
    # global pixmap_all
    pixmap_all = []
    # print(pixmap.isNull())
    while not pixmap.isNull():
        # pixmap_all.append(pixmap)
        index += 1
        n = str('_' + str(index + 1))
        next_url = url_s[0] + art + n + url_s[1]
        pixmap = load_image(next_url)
        # print(index, not pixmap.isNull(), next_url)
    return index - 1


def get_image(label, pixmap):
    # Отримати оригінальний розмір зображення
    original_width = pixmap.width()
    original_height = pixmap.height()

    # Отримати розміри label
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
    ui.horizontalScrollBar.setMaximum(count_image(me_art))


# ----------------------------------------------------------------------------------------------------------
# ---------------END ЗОБРАЖЕННЯ---------------------------------------------------------------------------------


tmp = []
file_tmp = open_price()
data = file_tmp[0]
len_dada = len(data)

setData(data)

r = str(ui.treeView.model().rowCount())
nm_prise = str(file_tmp[1]).split('.')[-2].split('/')[-1]

ui.label_PriceDataName.setText(nm_prise)
ui.label.setText('Кількість знайдених результатів: ' + r)
art_0 = ui.treeView.model().index(0, 0).data()

header = ui.treeView.header()

# --------------------Підключення сигналів-------------------------------------------------------------
ui.lineEdit_SearchName.textChanged.connect(find_in)
ui.lineEdit_SearchCategori.textChanged.connect(find_in)
ui.lineEdit_SearchArt.textChanged.connect(find_in)
ui.treeView.clicked.connect(treeView_clicked)
ui.treeView.doubleClicked.connect(treeView_doubleClicked)
header.sectionClicked.connect(handleHeaderClick)
header.sectionDoubleClicked.connect(handleHeaderDoubleClick)
Form.show()
update_image(art_0)
ui.horizontalScrollBar.valueChanged.connect(slider_change)


def retranslateUi(Form):
    _translate = QtCore.QCoreApplication.translate
    Form.setWindowTitle(_translate("Form", "Form"))


sys.exit(app.exec_())
