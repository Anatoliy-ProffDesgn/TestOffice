# ---------------ЗОБРАЖЕННЯ---------------------------------------------------------------------------------
import random

import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap

import inet_test

ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
]
url_s = ['https://viyar.ua/store/Items/photos/ph', '.jpg']


def load_first_image(art):
    url = url_s[0] + art + url_s[1]
    return load_image(url)


def load_image(url):
    pixmap = QPixmap()
    try:
        response = requests.get(url, headers={'User-Agent': random.choice(ua)})
        pixmap.loadFromData(response.content)
        return pixmap
    except:
        return pixmap


def count_image(art):
    pixmap = load_first_image(art)
    index = 0
    # global pixmap_all
    pixmap_all = []
    while not pixmap.isNull():
        pixmap_all.append(pixmap)
        index += 1
        n = str('_' + str(index + 1))
        next_url = url_s[0] + art + n + url_s[1]
        pixmap = load_image(next_url)
    # pixmap_all.append(index - 1)
    return pixmap_all


def get_image(label, pixmap):
    if inet_test.is_internet_available():
        # Отримати оригінальний розмір зображення
        original_width = pixmap.width()
        original_height = pixmap.height()
        # global label_width
        # global label_height
        # Отримати розміри label
        # if label_width == 0 or label_height == 0:
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
    else:
        label.setText('Перевірте підключення до мережі інтернет')
