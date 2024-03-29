import json as js
import datetime as d
import csv
import os

from PyQt5.QtGui import QStandardItem

import LoadPrice_main as Load_price
from Parse_html import full_price as f_price

global splash


# ---------------Load (and/or) Update and save in json------------------
def load_update(view, load_in_url=True, update_in_file=True, file_name=''):
    global splash
    if not os.path.isdir('./Price/'):
        os.makedirs('./Price/')
    if file_name == "":
        date = d.date.today().strftime("%d_%m_%Y")
        price_file_name = './Price/Віяр фурнітура прайс ' + date + '.json'
    else:
        price_file_name = file_name
    if load_in_url:
        urls = open_urls_csv()
        Load_price.download_price(urls, view)
    if update_in_file:
        with open(price_file_name, 'w', encoding='utf-8') as file:
            price = f_price('./temp/DownloadPrices/', view)
            js.dump(price, file)


def open_urls_csv(file_name='Shablon/URLs.csv'):
    url_s = []
    # Відкриваємо файл та читаємо url з кожного рядка
    with open(file_name, newline='', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, dialect=csv.excel)
        for row in reader:
            if row:
                url_s.append(row[0])
    return url_s


# print(prise_file_name)

# load_update(True, True)
def info_to_view(view, info_dict):
    model = view.model()
    item1 = QStandardItem(info_dict)
    model.appendRow(item1)
    view.setModel(model)
    view.show()
