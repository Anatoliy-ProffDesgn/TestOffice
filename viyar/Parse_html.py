# створено спираючись на інструкцію із https://python-scripts.com/beautifulsoup-html-parsing

# import requests
# from PyInstaller.isolated._parent import child
from bs4 import BeautifulSoup
from AllFile_inDir import get_file as get_file_list

f_name = './temp/newPrice1.html'


# ---------------парсим файл, формуєм [dict(),...,dict()] результатів--------------
def price_pars(file_name, e_cod='utf-8'):
    with open(file_name, "r", encoding=e_cod) as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        pr_title = str(soup.thead.tr.text)

        # видаляємо усе зайве з назви
        olds = ['  ', '\n', 'ПРАЙС-ЛИСТ на ']
        for old in olds:
            pr_title = pr_title.replace(old, '')
        pr_title = pr_title.split(' від ')[0]
        rez = []
        for tag in soup.tbody.find_all("tr"):
            tmp = str(tag.text).split('\n')
            tmp.pop(), tmp.pop(0)  # Видаляємо порожні (першу і останню) ел. списку
            price_val = tmp[len(tmp) - 2].split()  # Формуєм з '125,1 грн.' --> '125.2', 'грн/шт'
            if len(price_val) == 1:
                price_val = ['0', price_val[0]]
            tmp[len(tmp) - 2] = (price_val[0].replace(',', '.'))
            tmp[len(tmp) - 1] = price_val[1].replace('.', '') + '/' + tmp[len(tmp) - 1]
            d_rez = {'Article': tmp[0],
                     'Name': tmp[1],
                     'Price': tmp[2],
                     'Unit': tmp[3],
                     'Category': pr_title}
            rez.append(d_rez)
    return rez


# -----------перебираєм всі файли прайсів у теці, збираєм повний прайс-------------
def full_price(dir_name):
    files_list = get_file_list(dir_name, 'price', 'html')
    price = []
    for file in files_list:
        tmp_price = price_pars(file)
        for p in tmp_price:
            price.append(p)
    return price


# ------------Тест-----------------
# # rez1 = price_pars(f_name)
# # print(rez1)
# #
# # for lst in rez1:
# #     print(lst)
# # print(str(len(rez1)), '- строк(а)')
# i = 0
# price1 = full_price('./DownloadPrices/')
# for pr in price1:
#     i += 1
#     print(i, pr)
# print(str(len(price1)), '- строк(а)')
