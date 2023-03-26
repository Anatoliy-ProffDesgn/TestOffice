import threading
from threading import Lock
import requests
from bs4 import BeautifulSoup
import random
import inet_test
import time

from django.template.defaultfilters import pprint

ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
]

url = "https://viyar.ua/"


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
    with lock:
        print(me_str)


def me_parse_menu():
    t = time.time()
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
    print(f"Доступ до сайту за: {int((time.time() - t) // 60):02d}:{int((time.time() - t) % 60):02d}")
    # return new_lst
    print('____________Збираємо URLs прайсів по сторінках____________')
    list_load_link = me_parse_load_link(new_lst)
    print('____________Отримали URLs прайсів____________')
    print(f"Збір посилань завершена за: {int((time.time() - t) // 60):02d}:{int((time.time() - t) % 60):02d}")
    return list_load_link


def process_item(item, url):
    # print(item['cat'], '|', item['rozdil'])
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
            me_print_process(f'Отримано: {load_link} -> {item["cat"]} | {item["rozdil"]}')
            return d
        except:
            me_print_process(f'_______None link_______: {item["link"]} -> {item["cat"]} | {item["rozdil"]}')
            pass
    return None


def me_parse_load_link(lst):
    if lst is None:
        return None
    url = "https://viyar.ua/"
    new_lst = []
    threads = []
    for item in lst:
        t = threading.Thread(target=lambda: new_lst.append(process_item(item, url)))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return [item for item in new_lst if item is not None]


if __name__ == '__main__':
    lst = me_parse_menu()
    # me_print(lst)
    print(lst)
    print(len(lst))

# [{'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Cleaf', 'link': 'https://viyar.ua/excel_export/?id=2483&to_xls=Y&lang=ua'}, ...]
