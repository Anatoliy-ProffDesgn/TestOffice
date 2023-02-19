import json as js
import datetime as d
import LoadPrice_main as load_price
from Parse_html import full_price as f_price
import AllFile_inDir as a

up = input('завантажити з сайту (може тривати від декількох хвилин...) Y/n')
re = input('Переписати Прайс Y/n')
date = d.date.today().strftime("%d_%m_%Y")
price_file_name = './Price/Віяр фурнітура прайс ' + date + '.json'

if up.lower() == 'y':
    load_price.download_price()

if re.lower() == 'y':
    with open(price_file_name, 'w', encoding='utf-8') as f:
        price = f_price('./DownloadPrices/')
        js.dump(price, f)

# ---------------Open json------------------
f_name = a.get_file('./Price')
print(f_name[0])
with open(f_name[0], 'r', encoding='utf-8') as f:
    price = js.load(f)
    i = 0
    j = 0
    for p in price:
        i += 1
        search_str = 'зав'
        if (search_str.lower() in str(p['Name']).lower()) or (search_str.lower() in str(p['Category']).lower()):
            j += 1
            print(i, p)
    print('Знайдено', j)

# print(prise_file_name)
