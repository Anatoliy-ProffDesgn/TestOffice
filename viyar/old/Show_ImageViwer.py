# from ImageViwer import *
from Price_Window import *
import requests
from PyQt5.QtGui import QPixmap

url_s = ['https://viyar.ua/store/Items/photos/ph', '.jpg']

global me_art



def load_image(url):
    response = requests.get(url)
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
    get_image(ui.label, pixmap)


def count_image(art):
    pixmap = load_first_image(art)
    index = 0
    # print(pixmap.isNull())
    while not pixmap.isNull():
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
    label_width = ui.label.width()
    label_height = ui.label.height()

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
    get_image(ui.label, load_first_image(me_art))
    ui.horizontalScrollBar.setMaximum(count_image(me_art))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    # ui.setupUi(Form)

    update_image(ui.lineEdit_art.text())
    ui.horizontalScrollBar.valueChanged.connect(slider_change)


    Form.show()
    sys.exit(app.exec_())
