import json as js
import datetime as d
import LoadPrice_main as Load_price
from URL_list import url_list as urls
from Parse_html import full_price as f_price

# up = input('завантажити з сайту (може тривати від декількох хвилин...) Y/n')
# re = input('Переписати Прайс Y/n')
# if up.lower() == 'y':
#     up = True
# else:
#     up = False
# if re.lower() == 'y':
#     re = True
# else:
#     re = False


# ---------------Load (and/or) Update and save in json------------------
def load_update(load_in_url=True, update_in_file=True, file_name=''):
    if file_name == "":
        date = d.date.today().strftime("%d_%m_%Y")
        price_file_name = './Price/Віяр фурнітура прайс ' + date + '.json'
    if load_in_url:
        Load_price.download_price(urls)
    if update_in_file:
        with open(price_file_name, 'w', encoding='utf-8') as file:
            price = f_price('./DownloadPrices/')
            js.dump(price, file)

# print(prise_file_name)

load_update(False, True)
