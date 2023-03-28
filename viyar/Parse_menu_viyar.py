# -*- coding: utf-8 -*-
import multiprocessing as mp
import sys
import threading
import time
import traceback
from functools import partial
from threading import Lock
import requests
from bs4 import BeautifulSoup
import random
import inet_test
from datetime import datetime as dt
import DataBase as db


ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
]

url = "https://viyar.ua/"

def format_time(start_time):
    end_time = dt.now()
    time_diff = end_time - start_time
    seconds = int(time_diff.total_seconds())
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

def create_dct(categories, rozdil, links):
    dct = {}
    dct['cat'] = categories
    dct['rozdil'] = rozdil
    dct['link'] = links
    return dct


def me_print(lst):
    for item in lst:
        print(item['cat'], '|', item['rozdil'], '||', item['link'])  # , ' | len=', len(lst))
    # print(len(lst))
    # input('Натисніть клавішу для завершення')


lock = Lock()


def me_print_process(me_str):
    # with lock:
        print(me_str)


def me_parse_menu():
    start_time = dt.now()
    if not inet_test.is_internet_available():
        return None
    print('____________Отримуэмо доступ до сайту____________')
    response = requests.get(url, headers={'User-Agent': random.choice(ua)})

    soup = BeautifulSoup(response.text, "html.parser")
    dropdown = soup.find_all("li", {"class": "dropdown__list-item_lev1"})
    i = 0
    # pprint(dropdown)
    lst = []

    for item in dropdown:
        i += 1
        # Отримуємо назву та посилання dropdown-елемента рівня 1
        name_lev1 = item.find("a").text.strip()
        link_lev1 = item.find("a")["href"]
        # print('_______________')
        # print(f' {i}', name_lev1, '||', link_lev1)
        # Отримуємо всі dropdown-елементи рівня 2 та їхні назви та посилання
        items_lev2 = item.find_all("li", {"class": "dropdown__list-item li_lev2"})
        # if len(items_lev2) == 0:
        #     items_lev2 = item.find_all("li", {"class": "dropdown__list-item lastLevel-item"})
        lst.append(create_dct(name_lev1, name_lev1, link_lev1)) if len(items_lev2) == 0 else None
        j = 0
        for item2 in items_lev2:
            j += 1
            name_lev2 = item2.find("a").text.strip()
            link_lev2 = item2.find("a")["href"]
            # print(f'    {i, j}', name_lev1, '|', name_lev2, '||', link_lev2)
            items_lev3 = item2.find_all("li", {"class": "dropdown__list-item"})
            lst.append(create_dct(name_lev1, name_lev2, link_lev2)) if len(items_lev3) == 0 else None
            c = 0
            for item3 in items_lev3:
                c += 1
                name_lev3 = item3.find("a").text.strip()
                link_lev3 = item3.find("a")["href"]
                # print(f'        {i, j, c}', name_lev1, '|', name_lev2, '|', name_lev3, '||', link_lev3)
                lst.append(create_dct(name_lev1, name_lev2 + ' | ' + name_lev3, link_lev3))
    new_lst = []
    for item in lst:  # видаляємо дублікати з масиву
        if item not in new_lst:
            new_lst.append(item)
    for item in new_lst:
        item['link'] = item['link'][1:] if item['link'][0] == '/' else item['link']
        item['link'] = url + item['link'] if not 'https://' in item['link'] else item['link']
    print(f"Доступ до сайту за: {format_time(start_time)}")
    # return new_lst
    print('____________Збираємо URLs прайсів по сторінках____________')
    list_load_link = me_parse_load_link(new_lst)
    print('____________Отримали URLs прайсів____________')
    print(f"Збір посилань завершена за: {format_time(start_time)}")
    return list_load_link


def process_item(item, url):
    # print(item['cat'], '|', item['rozdil'])
    me_base = db.DataBase('DataBase.db')
    p_time = dt.now()
    if url in item['link']:
        response = requests.get(item['link'], headers={'User-Agent': random.choice(ua)})
        soup = BeautifulSoup(response.text, "html.parser")
        buttons = soup.find("a", {"class": "button button--transparent"})

        # pprint(buttons)
        try:
            load_link = buttons.get("href")
            load_link = url + load_link[1:] if load_link[0] == '/' else url + load_link
            d = create_dct(item['cat'], item['rozdil'], load_link)
            # str_rez = str(f'Отримано: {load_link} -> {item["cat"]} | {item["rozdil"]}\n')
            # with lock:
            print(f'{format_time(p_time)} Отримано: {load_link} -> {item["cat"]} | {item["rozdil"]}')
            me_base.create_table_text('log_update_26_03_2023', d, False)
            print(f'Отримано: {load_link} -> {item["cat"]} | {item["rozdil"]}')
            return d
        except:
            me_print_process(f'{format_time(p_time)}_______None link_______: {item["link"]} -> {item["cat"]} | {item["rozdil"]}')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Exception type:", exc_type)
            print("Exception message:", exc_value)
            print("Exception traceback:", exc_traceback)
            pass
    return None


def me_parse_load_link(lst):
    if lst is None:
        return None
    url = "https://viyar.ua/"
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = [pool.apply_async(process_item, args=(item, url)) for item in lst]
        new_lst = [r.get() for r in results if r.get() is not None]
    return new_lst

def price_pars(soup, row):
    rez = []
    me_db = db.DataBase('DataBase.db')
    if not 'viyar.ua | 524: A timeout occurred' in soup:
        for tag in soup.tbody.find_all("tr"):
            tmp = str(tag.text).split('\n')
            tmp.pop(), tmp.pop(0)  # Видаляємо порожні (першу і останню) ел. списку
            price_val = tmp[len(tmp) - 2].split()  # Формуєм з '125,1 грн.' --> '125.2', 'грн/шт'
            if len(price_val) == 1:
                price_val = ['0', price_val[0]]
            tmp[len(tmp) - 2] = (price_val[0].replace(',', '.'))
            tmp[len(tmp) - 1] = price_val[1].replace('.', '') + '/' + tmp[len(tmp) - 1]
            if ' | ' in row['rozdil']:
                subcat = row['rozdil'].split(' | ')
            else:
                subcat = [row['rozdil'], row['rozdil']]
            # (article, name, price, quality, category, subcategory, subsubcategory, image, )
            d_rez = {'article': tmp[0],
                     'name': tmp[1],
                     'price': tmp[2],
                     'quality': tmp[3],
                     'category': row['cat'],
                     'subcategory': subcat[0],
                     'subsubcategory': subcat[1],
                     'image': None,
                     'data': None}
            rez.append(d_rez)
        for r in rez:
            me_db.insert_into_price('price_26_03_2023', r)
    return rez

def download_and_parse(row):
    t = dt.now()
    # print("Process start")
    # print(f"Process start")
    try:
        url = row['link']
        # завантаження HTML сторінки
        # print('завантаження HTML сторінки')
        response = requests.get(url)
        html = response.text
        # витягнення таблиці
        # print('початок soup = BeautifulSoup')
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        # print('витягнення таблиці у dicts')
        dicts = price_pars(soup, row)
        # print(dicts)
        print('++', format_time(t), row)
        return dicts
    except Exception as e:
        traceback.print_exc()
        print('--', format_time(t), row)
        return None


# функція для обробки помилок
def handle_error(e):
    traceback.print_exc()


def update_full_prise():
    t=dt.now()
    me_db = db.DataBase('DataBase.db')
    rows = me_db.select_from_table('log_update_26_03_2023')
    # зберігаємо функцію download_and_parse з фіксованим аргументом row
    download_and_parse_row = partial(download_and_parse)
    num_processors = mp.cpu_count()
    # print(rows)
    for row in rows:
        with mp.Pool(3) as pool:
            # виконання download_and_parse_row для кожного рядка з бази даних у окремому процесі
            # обробка помилок викликає функцію handle_error
            dict_row = dict(row)
            print(format_time(t), 'Новий поцес')
            # print(f"Number of active processes: {len(mp.active_children())}")
            pool.apply_async(download_and_parse_row, (dict_row,), error_callback=handle_error)
            # чекаємо, поки процес завершиться
            pool.close()
            pool.join()
    print(format_time(t), 'Завершено')



if __name__ == '__main__':
    update_full_prise()
    # lst = me_parse_menu()
    # me_db = db.DataBase('DataBase.db')
    # download_and_parse(me_db.select_row_by_id('log_update_26_03_2023', 1))
    # me_print(lst)
    # lst = [{'cat': 'Плитні матеріали', 'rozdil': 'ХДФ / ДВП | ДВП Уніплит', 'link': 'https://viyar.ua/excel_export/?id=3239&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Swiss Krono', 'link': 'https://viyar.ua/excel_export/?id=2492&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | AGT', 'link': 'https://viyar.ua/excel_export/?id=2510&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | Kronospan', 'link': 'https://viyar.ua/excel_export/?id=2512&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Навіси меблеві', 'link': 'https://viyar.ua/excel_export/?id=2540&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки для отворів під ручку', 'link': 'https://viyar.ua/excel_export/?id=3287&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | Панелі МДФ Cleaf Piombo', 'link': 'https://viyar.ua/excel_export/?id=3161&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Різні метизи', 'link': 'https://viyar.ua/excel_export/?id=2529&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Тримачі дзеркал', 'link': 'https://viyar.ua/excel_export/?id=3309&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки для завіс', 'link': 'https://viyar.ua/excel_export/?id=3288&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Завіси й аксесуари | Аксесуари', 'link': 'https://viyar.ua/excel_export/?id=2567&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Дюбелі', 'link': 'https://viyar.ua/excel_export/?id=2524&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Герметики, силікони', 'link': 'https://viyar.ua/excel_export/?id=3073&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Ніжки, ролики, опори | Ніжки', 'link': 'https://viyar.ua/excel_export/?id=2546&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | МДФ (інші)', 'link': 'https://viyar.ua/excel_export/?id=2988&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Консолі', 'link': 'https://viyar.ua/excel_export/?id=3311&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки для саморізів', 'link': 'https://viyar.ua/excel_export/?id=3290&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Ніжки, ролики, опори | Опори', 'link': 'https://viyar.ua/excel_export/?id=2548&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Комплектуючі для ліжок | Каркаси для ліжок', 'link': 'https://viyar.ua/excel_export/?id=2982&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Завіси й аксесуари | Завіси', 'link': 'https://viyar.ua/excel_export/?id=2566&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': "Панелі для інтер'єру | Панелі HAUTE MATERIAL", 'link': 'https://viyar.ua/excel_export/?id=2518&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Ручки та гачки | Ручки-профіль', 'link': 'https://viyar.ua/excel_export/?id=2544&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Борти кухонні і цоколі | Цоколі та комплектуючі', 'link': 'https://viyar.ua/excel_export/?id=2570&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Релінги і комплектуючі | Релінги та кріплення', 'link': 'https://viyar.ua/excel_export/?id=2564&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Пакувальний матеріал | Стретч', 'link': 'https://viyar.ua/excel_export/?id=3209&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Комплектуючі для ліжок | Підйомні механізми для ліжок', 'link': 'https://viyar.ua/excel_export/?id=2983&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Клей HENKEL', 'link': 'https://viyar.ua/excel_export/?id=2583&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Вентиляційні решітки', 'link': 'https://viyar.ua/excel_export/?id=3286&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | DDL', 'link': 'https://viyar.ua/excel_export/?id=3079&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Конфірмати', 'link': 'https://viyar.ua/excel_export/?id=2525&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Комплектуючі для модульної системи | Scilm', 'link': 'https://viyar.ua/excel_export/?id=3148&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Шухляди MullerBox', 'link': 'https://viyar.ua/excel_export/?id=2535&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Ручки та гачки | Профілі Gola', 'link': 'https://viyar.ua/excel_export/?id=3277&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | Kastamonu', 'link': 'https://viyar.ua/excel_export/?id=3131&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Тримачі для полиць', 'link': 'https://viyar.ua/excel_export/?id=3308&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Клей двокомпонентний', 'link': 'https://viyar.ua/excel_export/?id=3074&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки для дротів', 'link': 'https://viyar.ua/excel_export/?id=3289&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Метабокси', 'link': 'https://viyar.ua/excel_export/?id=2532&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Сушки і піддони', 'link': 'https://viyar.ua/excel_export/?id=2542&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Ніжки, ролики, опори | Ролики', 'link': 'https://viyar.ua/excel_export/?id=2547&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки самоклеючі', 'link': 'https://viyar.ua/excel_export/?id=3292&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'ХДФ / ДВП | ХДФ Pfleiderer', 'link': 'https://viyar.ua/excel_export/?id=2508&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'Пластик HPL | Fenix', 'link': 'https://viyar.ua/excel_export/?id=2919&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Шухляди ArciTech', 'link': 'https://viyar.ua/excel_export/?id=2533&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | Kronospan', 'link': 'https://viyar.ua/excel_export/?id=2607&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Кошики, відра, магічні кути', 'link': 'https://viyar.ua/excel_export/?id=2539&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Кабінетні куточки', 'link': 'https://viyar.ua/excel_export/?id=3310&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Пакувальний матеріал | Скотч', 'link': 'https://viyar.ua/excel_export/?id=3210&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': "Панелі для інтер'єру | Стінові панелі AGT", 'link': 'https://viyar.ua/excel_export/?id=2937&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Направляючі', 'link': 'https://viyar.ua/excel_export/?id=2531&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Релінги і комплектуючі | Полиці для релінгу', 'link': 'https://viyar.ua/excel_export/?id=2563&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Колони', 'link': 'https://viyar.ua/excel_export/?id=2728&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Саморізи', 'link': 'https://viyar.ua/excel_export/?id=2528&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки пластикові', 'link': 'https://viyar.ua/excel_export/?id=3291&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Накладки для стільниць', 'link': 'https://viyar.ua/excel_export/?id=2541&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | Niemann', 'link': 'https://viyar.ua/excel_export/?id=2495&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'ХДФ / ДВП | ХДФ Kronospan', 'link': 'https://viyar.ua/excel_export/?id=2507&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Ніжки, ролики, опори | Допоміжна фурнітура', 'link': 'https://viyar.ua/excel_export/?id=2549&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'Пластик HPL | Arpa', 'link': 'https://viyar.ua/excel_export/?id=2920&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'Фанера | Фанера вологостійка', 'link': 'https://viyar.ua/excel_export/?id=2520&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'OSB | OSB/3 Swiss Krono', 'link': 'https://viyar.ua/excel_export/?id=2516&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | Egger', 'link': 'https://viyar.ua/excel_export/?id=2511&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Комплектуючі для модульної системи | Cosma', 'link': 'https://viyar.ua/excel_export/?id=3149&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Ручки та гачки | Гачки меблеві', 'link': 'https://viyar.ua/excel_export/?id=2560&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Організації для висувних шухляд', 'link': 'https://viyar.ua/excel_export/?id=3049&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Шухляди Atira', 'link': 'https://viyar.ua/excel_export/?id=2536&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Монтажні куточки', 'link': 'https://viyar.ua/excel_export/?id=3312&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Egger', 'link': 'https://viyar.ua/excel_export/?id=2484&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Шухляди AvanTech YOU', 'link': 'https://viyar.ua/excel_export/?id=2990&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Карго', 'link': 'https://viyar.ua/excel_export/?id=2538&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Стяжки', 'link': 'https://viyar.ua/excel_export/?id=2527&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Клей для стільниць', 'link': 'https://viyar.ua/excel_export/?id=2584&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Kronospan', 'link': 'https://viyar.ua/excel_export/?id=2490&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | Лаковані панелі МДФ', 'link': 'https://viyar.ua/excel_export/?id=2806&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | Коростень', 'link': 'https://viyar.ua/excel_export/?id=2513&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Гвинти', 'link': 'https://viyar.ua/excel_export/?id=2523&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Saviola', 'link': 'https://viyar.ua/excel_export/?id=2493&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Муфти', 'link': 'https://viyar.ua/excel_export/?id=2526&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стінові панелі | Kronospan', 'link': 'https://viyar.ua/excel_export/?id=2615&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | Панелі МДФ RAUVISIO Crystal', 'link': 'https://viyar.ua/excel_export/?id=2499&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | RICCI', 'link': 'https://viyar.ua/excel_export/?id=2773&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Борти кухонні і цоколі | Бортики кухонні і комплектуючі', 'link': 'https://viyar.ua/excel_export/?id=2569&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Ручки та гачки | Ручки меблеві', 'link': 'https://viyar.ua/excel_export/?id=2561&to_xls=Y&lang=ua'}, {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Клей монтажний', 'link': 'https://viyar.ua/excel_export/?id=3075&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Компакт-плита | Egger', 'link': 'https://viyar.ua/excel_export/?id=3186&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Компакт-плита | Fenix', 'link': 'https://viyar.ua/excel_export/?id=3184&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | RICCI', 'link': 'https://viyar.ua/excel_export/?id=2949&to_xls=Y&lang=ua'}, {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Cleaf', 'link': 'https://viyar.ua/excel_export/?id=2483&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | Arpa', 'link': 'https://viyar.ua/excel_export/?id=2609&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Kromag', 'link': 'https://viyar.ua/excel_export/?id=2591&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стінові панелі | LuxeForm', 'link': 'https://viyar.ua/excel_export/?id=2614&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | Egger', 'link': 'https://viyar.ua/excel_export/?id=2611&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Egger', 'link': 'https://viyar.ua/excel_export/?id=2883&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | LuxeForm', 'link': 'https://viyar.ua/excel_export/?id=2608&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стінові панелі | Egger', 'link': 'https://viyar.ua/excel_export/?id=2613&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Rehau', 'link': 'https://viyar.ua/excel_export/?id=2588&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Компакт-плита | Arpa', 'link': 'https://viyar.ua/excel_export/?id=3180&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Амбарний механізм', 'link': 'https://viyar.ua/excel_export/?id=2780&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Swiss Krono', 'link': 'https://viyar.ua/excel_export/?id=2601&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Компакт-плита | Fundermax', 'link': 'https://viyar.ua/excel_export/?id=3185&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Arpa', 'link': 'https://viyar.ua/excel_export/?id=2599&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стінові панелі | Arpa', 'link': 'https://viyar.ua/excel_export/?id=2929&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Kronospan', 'link': 'https://viyar.ua/excel_export/?id=2602&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Luxeform', 'link': 'https://viyar.ua/excel_export/?id=2600&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Niemann', 'link': 'https://viyar.ua/excel_export/?id=2593&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Шпонована', 'link': 'https://viyar.ua/excel_export/?id=2905&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Направляючий профіль', 'link': 'https://viyar.ua/excel_export/?id=2873&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Rehau лазерна', 'link': 'https://viyar.ua/excel_export/?id=2595&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Maag', 'link': 'https://viyar.ua/excel_export/?id=3169&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Hranipex', 'link': 'https://viyar.ua/excel_export/?id=2592&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Polkemic', 'link': 'https://viyar.ua/excel_export/?id=2943&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Вертикальний профіль', 'link': 'https://viyar.ua/excel_export/?id=2627&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Меламінова з клеєм', 'link': 'https://viyar.ua/excel_export/?id=2597&to_xls=Y&lang=ua'}, {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | Swiss Krono', 'link': 'https://viyar.ua/excel_export/?id=2610&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Фурнітура для розсувної системи', 'link': 'https://viyar.ua/excel_export/?id=2643&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Egger', 'link': 'https://viyar.ua/excel_export/?id=2589&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Складна система Starke-W', 'link': 'https://viyar.ua/excel_export/?id=2896&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Профіль Connect', 'link': 'https://viyar.ua/excel_export/?id=2644&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Розсувна система SlideLine 55', 'link': 'https://viyar.ua/excel_export/?id=2648&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Складна система WingLine 230', 'link': 'https://viyar.ua/excel_export/?id=2653&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Складна система WingLine L', 'link': 'https://viyar.ua/excel_export/?id=2772&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | AGT', 'link': 'https://viyar.ua/excel_export/?id=2594&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Розсувна система TopLine XL v2.0', 'link': 'https://viyar.ua/excel_export/?id=3047&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Terno Scorrevoli | Розсувна система Dama', 'link': 'https://viyar.ua/excel_export/?id=3121&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Профіль Compact', 'link': 'https://viyar.ua/excel_export/?id=2925&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Аксесуари', 'link': 'https://viyar.ua/excel_export/?id=2651&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Ario | Супутня фурнітура Ario', 'link': 'https://viyar.ua/excel_export/?id=2658&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Розсувна система Glatt', 'link': 'https://viyar.ua/excel_export/?id=2645&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Гардеробна система Eureka | Комплектуючі Eureka', 'link': 'https://viyar.ua/excel_export/?id=2795&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Ario | Направляючий профіль Ario', 'link': 'https://viyar.ua/excel_export/?id=2657&to_xls=Y&lang=ua'}, {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Cleaf', 'link': 'https://viyar.ua/excel_export/?id=2590&to_xls=Y&lang=ua'}, {'cat': 'Меблі', 'rozdil': 'Готові дзеркала | Дзеркала без підсвічування', 'link': 'https://viyar.ua/excel_export/?id=3243&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Ario | Горизонтальний профіль Ario', 'link': 'https://viyar.ua/excel_export/?id=2656&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Розсувна система TopLine L v2.0', 'link': 'https://viyar.ua/excel_export/?id=3046&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Кухонні комплектуючі | Фільтри для води Ecosoft', 'link': 'https://viyar.ua/excel_export/?id=2821&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Ario | Вертикальний профіль Ario', 'link': 'https://viyar.ua/excel_export/?id=2655&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Міжкімнатні системи Terno Scorrevoli | Розсувна система Diva air Vetro', 'link': 'https://viyar.ua/excel_export/?id=3123&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Горизонтальний профіль', 'link': 'https://viyar.ua/excel_export/?id=2634&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Terno Scorrevoli | Компланарна система Switch', 'link': 'https://viyar.ua/excel_export/?id=3117&to_xls=Y&lang=ua'}, {'cat': 'Скло та дзеркало', 'rozdil': 'Скло та дзеркало', 'link': 'https://viyar.ua/excel_export/?id=2514&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Розсувна система SlideLine M', 'link': 'https://viyar.ua/excel_export/?id=2652&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Кавомашини', 'link': 'https://viyar.ua/excel_export/?id=2998&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Міжкімнатні системи Terno Scorrevoli | Розсувна система Magic 2', 'link': 'https://viyar.ua/excel_export/?id=3119&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Міжкімнатні системи Terno Scorrevoli | Розсувна система Vetro 40', 'link': 'https://viyar.ua/excel_export/?id=3125&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Гардеробна система Eureka | Комплекти Eureka', 'link': 'https://viyar.ua/excel_export/?id=3165&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Варильні поверхні', 'link': 'https://viyar.ua/excel_export/?id=2955&to_xls=Y&lang=ua'}, {'cat': 'Меблі', 'rozdil': 'Готові дзеркала | Дзеркала з підсвічуванням', 'link': 'https://viyar.ua/excel_export/?id=3267&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Кухонні плити', 'link': 'https://viyar.ua/excel_export/?id=3316&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Холодильна техніка', 'link': 'https://viyar.ua/excel_export/?id=2968&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Мікрохвильові печі', 'link': 'https://viyar.ua/excel_export/?id=2958&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Витяжки', 'link': 'https://viyar.ua/excel_export/?id=2683&to_xls=Y&lang=ua'}, {'cat': 'Вироби з каменю', 'rozdil': 'Кварцит | Caesarstone', 'link': 'https://viyar.ua/excel_export/?id=3194&to_xls=Y&lang=ua'}, {'cat': 'Вироби з каменю', 'rozdil': 'Широкоформатний керамограніт | Inalco', 'link': 'https://viyar.ua/excel_export/?id=3196&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Кухонні комплектуючі | Вентиляційні системи', 'link': 'https://viyar.ua/excel_export/?id=2798&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Кухонні комплектуючі | Мийки та аксесуари', 'link': 'https://viyar.ua/excel_export/?id=2676&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Кухонні комплектуючі | Змішувачі', 'link': 'https://viyar.ua/excel_export/?id=2691&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Пральні машини', 'link': 'https://viyar.ua/excel_export/?id=2967&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Фурнітура для встановлення вбудованої техніки', 'link': 'https://viyar.ua/excel_export/?id=3226&to_xls=Y&lang=ua'}, {'cat': 'Вироби з каменю', 'rozdil': 'Штучний акриловий камінь | Grandex', 'link': 'https://viyar.ua/excel_export/?id=3233&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Підкладки | ДВП', 'link': 'https://viyar.ua/excel_export/?id=3100&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Посудомийні машини', 'link': 'https://viyar.ua/excel_export/?id=2743&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Коркове покриття | Egger Comfort', 'link': 'https://viyar.ua/excel_export/?id=3114&to_xls=Y&lang=ua'}, {'cat': 'Вироби з металу', 'rozdil': 'Вироби з металу', 'link': 'https://viyar.ua/excel_export/?id=3257&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Композитне покриття | Egger Design GreenTec', 'link': 'https://viyar.ua/excel_export/?id=3111&to_xls=Y&lang=ua'}, {'cat': 'Вироби з каменю', 'rozdil': 'Широкоформатний керамограніт | Neolith', 'link': 'https://viyar.ua/excel_export/?id=3195&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Підкладки | Коркова', 'link': 'https://viyar.ua/excel_export/?id=3099&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Плінтуси та комплектуючі | KAINDL', 'link': 'https://viyar.ua/excel_export/?id=3096&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Духові шафи', 'link': 'https://viyar.ua/excel_export/?id=2957&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Ламінат | CLASSEN', 'link': 'https://viyar.ua/excel_export/?id=3154&to_xls=Y&lang=ua'}, {'cat': 'Вироби з каменю', 'rozdil': 'Штучний акриловий камінь | Getacore', 'link': 'https://viyar.ua/excel_export/?id=3263&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Ламінат | KRONOPOL', 'link': 'https://viyar.ua/excel_export/?id=3155&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Плінтуси та комплектуючі | FN Neuhofer Holz', 'link': 'https://viyar.ua/excel_export/?id=3095&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Ламінат | KAINDL', 'link': 'https://viyar.ua/excel_export/?id=3091&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Ламінат | EGGER', 'link': 'https://viyar.ua/excel_export/?id=3092&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Плінтуси та комплектуючі | Arbiton', 'link': 'https://viyar.ua/excel_export/?id=3204&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Підкладки | Полістирольна', 'link': 'https://viyar.ua/excel_export/?id=3098&to_xls=Y&lang=ua'}, {'cat': 'Освітлення для меблів', 'rozdil': 'Освітлення для меблів', 'link': 'https://viyar.ua/excel_export/?id=2550&to_xls=Y&lang=ua'}, {'cat': 'Інструменти і витратні матеріали', 'rozdil': 'Інструменти і витратні матеріали', 'link': 'https://viyar.ua/excel_export/?id=2574&to_xls=Y&lang=ua'}, {'cat': 'Покриття підлоги', 'rozdil': 'Плінтуси та комплектуючі | Cezar', 'link': 'https://viyar.ua/excel_export/?id=3094&to_xls=Y&lang=ua'}, {'cat': 'Виробничі послуги', 'rozdil': 'Виробничі послуги', 'link': 'https://viyar.ua/excel_export/?id=2694&to_xls=Y&lang=ua'}]
    # print(lst)
    # me_base = db.DataBase('DataBase.db')
    # table_name = 'test_log_update_27_03_2023'
    # if table_name in me_base.get_table_list():
    #     me_base.delete_table(table_name)
    # me_base.create_table_text(table_name, lst)
    # print(len(lst))


