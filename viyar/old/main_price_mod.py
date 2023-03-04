import random
import sys

import requests
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItemModel, QDesktopServices
from PyQt5.QtWidgets import QInputDialog, QTreeView

import img_viwer
from Open_Price import open_price
from Price_Window import *
from Search_txt_in_price import find_txt_in_price
from main_Full_Updete_Price import *


class MyTreeViewPrice(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            print("Space key pressed")
        else:
            super().keyPressEvent(event)

class MyForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_img.mouseDoubleClickEvent = self.viwe_img

        model = QtGui.QStandardItemModel()
        self.ui.treeView.setModel(model)

        tree_size_policy = self.ui.treeView.sizePolicy()
        tree_geometry = self.ui.treeView.geometry()
        print('tree_size_policy',tree_size_policy)
        print('tree_geometry',tree_geometry)
        self.ui.myTreeViewPrice = MyTreeViewPrice(self.ui.gridLayoutWidget)
        self.ui.myTreeViewPrice.setSizePolicy(tree_size_policy)
        self.ui.myTreeViewPrice.setGeometry(tree_geometry)

        # self.ui.gridLayoutWidget.addWidget(self.ui.myTreeViewPrice)

        self.ui.treeView.keyPressEvent = self.me_keyPressEvent
        self.ui.treeView.installEventFilter(self)

    def me_keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            print('me_keyPressEvent', event.key())
        else:
            self.parent().keyPressEvent(event)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Space:
                print('eventFilter', event.key())
            else:
                return super().eventFilter(source, event)
        else:
            return super().eventFilter(source, event)

    def viwe_img(self, pixmap_all, index):
        index = 0 if index > len(pixmap_all) else index
        global indx
        indx = index
        pixmap = QPixmap(pixmap_all[index])  # ui.horizontalScrollBar.value()
        img_viwer.Form_viwer = QtWidgets.QWidget()
        ui_viwer = img_viwer.Ui_Form_viwer()
        ui_viwer.setupUi(img_viwer.Form_viwer)
        ui_viwer.label.setPixmap(pixmap)
        img_viwer.Form_viwer.show()
        app.exec_()


# ui.treeView.keyPressEvent = ui.treeView.keyPressEvent



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
# Form = QtWidgets.QWidget()
Form = MyForm()
ui = Ui_Form()
ui.setupUi(Form)
# -----------Створюємо модель даних і встановлюємо її в treeView-------------------------------------------
ui.model = QtGui.QStandardItemModel()
ui.treeView = MyTreeViewPrice(ui.treeView)

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
    clear_model(ui.treeView, ui.model)
    # interior(ui.model, ui.treeView)
    ui.model.invisibleRootItem().clearData()
    for item in data_rez:
        root = ui.model.invisibleRootItem()
        root.appendRow([QtGui.QStandardItem(item['Article']),
                        QtGui.QStandardItem(item['Name']),
                        QtGui.QStandardItem(item['Price']),
                        QtGui.QStandardItem(item['Unit']),
                        QtGui.QStandardItem(item['Category'])])
    # print(ui.model.rowCount())
    ui.treeView.setModel(ui.model)
    # ui.treeView.setSortingEnabled(True)

    ui.retranslateUi(Form)
    QtCore.QMetaObject.connectSlotsByName(Form)
    me_sort_mod(ui.model_null, ui.treeView_2)
    interior(ui.model_null, ui.treeView_2)
    ui.model_null.setHorizontalHeaderLabels(['Артикул', 'Назва виробу', 'Ціна', 'Одиниці', 'Кількість'])
    ui.treeView_2.setModel(ui.model_null)


def clear_model(me_treeview, me_model):
    me_model.removeRows(0, me_model.rowCount())
    me_treeview.setModel(me_model)


# -----------------функція пошуку по назві-----------------------------------------------------
def find_in():
    global data
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
    # print(len(data_2),len_data)
    # if len(data_2) != len_data or len(txt) != 0:
    ui.model2 = QStandardItemModel()
    interior(ui.model2, ui.treeView)
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
    # вивести модель
    ui.treeView.show()


# -----------------Метод для обробки clicked на елементі treeView-----------------------------------
def treeView_clicked(index):
    global art_old
    my_model = index.model()
    row = index.row()
    art = my_model.index(row, 0).data()  # отримуємо артикул
    if art != art_old:
        art_old = art
        update_image(art)


# ----------------Метод для обробки подвійного doubleClicked на елементі treeView-----------------
def treeView_doubleClicked(index):
    my_model = index.model()
    """
    Обробляє подвійний клік на записі у treeView1.
    Додає відповідний запис до treeView2.
    """
    # Отримати дані виділеної строки treeView1
    row_data = [my_model.data(my_model.index(index.row(), column)) for column in range(my_model.columnCount())]
    print(row_data)
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
    me_sort_mod(ui.model, ui.treeView)
    # print(f'Header clicked: column {index}')


# ----------------------------------------------------------------------------------------------------------
# ---------------ЗОБРАЖЕННЯ---------------------------------------------------------------------------------


def load_image(url):
    response = requests.get(url, headers={'User-Agent': random.choice(ua)})
    pixmap = QPixmap()
    pixmap.loadFromData(response.content)
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
    # print('--> count_image')
    while not pixmap.isNull():
        pixmap_all.append(pixmap)
        index += 1
        n = str('_' + str(index + 1))
        next_url = url_s[0] + art + n + url_s[1]
        pixmap = load_image(next_url)
        # print(index, not pixmap.isNull(), next_url)
    # print('count_image -->')
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
        with open('../temp/img_not.jpg', "rb") as f:
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

    # ui.treeView = MyTreeViewPrice()
    ui.treeView.setSortingEnabled(True)
    interior(ui.model, ui.treeView)

    setData(data)

    r = str(ui.treeView.model().rowCount())
    nm_prise = str(file_tmp[1]).split('.')[-2].split('/')[-1]

    ui.label_PriceDataName.setText(nm_prise)
    ui.label.setText('Кількість знайдених результатів: ' + r)
    art_0 = ui.treeView.model().index(0, 0).data()


# --------------------Підключення сигналів-------------------------------------------------------------
ui.lineEdit_SearchName.textChanged.connect(find_in)
ui.lineEdit_SearchCategori.textChanged.connect(find_in)
ui.lineEdit_SearchArt.textChanged.connect(find_in)

ui.treeView.clicked.connect(treeView_clicked)
ui.treeView.doubleClicked.connect(treeView_doubleClicked)
# ui.treeView.keyPressEvent = ui.treeView.keyPressEvent

ui.treeView_2.clicked.connect(treeView_clicked)
ui.treeView_2.doubleClicked.connect(treeView_del_selection_row)

ui.pushButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(ui.label_5.text())))
ui.pushButton_Update.clicked.connect(lambda: update_price(True))
ui.pushButton_Clear.clicked.connect(lambda: clear_model(ui.treeView_2, ui.model_null))

ui.label_img.mouseDoubleClickEvent = lambda event: MyForm().viwe_img(pixmap_all, ui.horizontalScrollBar.value())

header = ui.treeView.header()
header.sectionClicked.connect(handleHeaderClick)

if __name__ == "__main__":
    start()

Form.show()
update_image(art_0)
ui.horizontalScrollBar.valueChanged.connect(slider_change)

sys.exit(app.exec_())
