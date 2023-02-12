# downlod price from internet

import requests
import json
import os
import sys
from re import search
import urllib.request
import wget
#
url_ua = 'https://viyar.ua/excel_export/?id=2521&lang=ua'
url_ru = 'https://viyar.ua/excel_export/?id=1981&lang=ru'
#         https://viyar.ua/excel_export/?id=1981&lang=ru


def downlod_price(url, path, name='', typeFile='csv'):
    if name == '':  # перевірка чи не вказано ім'я файлу
        name = url.split('/')[-1]

    # перевірка недопустимих символів в імені файлу
    if search('[<>:"/\|?*&=]', name):
        for s in ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '&', '=']:
            name = name.replace(s, '')
        name = name.replace(' ', '_')

    # додати розширення typeFile якщо не вказано інше
    if name.split('.')[0] == name:
        name = name + '.' + typeFile

    if typeFile != 'csv':
        name = name.split('.')[0] + '.' + typeFile

    # створюємо папку, якщо її немає
    if not os.path.exists(path):
        os.makedirs(path)
    print(name)
    # завантажуємо файл з веб-сторінки
    r = requests.get(url, allow_redirects=True)
    # зберігаємо файл в файлову систему
    with open(path + '/' + name, 'wb') as f:
        f.write(r.content)


downlod_price('https://viyar.ua/store/Items/photos/ph69285.jpg', './temp/')
#urllib.request.urlretrieve('https://viyar.ua/excel_export/?id=2521&to_xls=Y&lang=ua', 'prs.xls')
wget.download('https://viyar.ua/store/Items/photos/ph69285.jpg', 'prs.jpg', bar =

