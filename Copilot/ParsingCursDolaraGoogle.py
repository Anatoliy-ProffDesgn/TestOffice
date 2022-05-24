import requests, datetime
from bs4 import BeautifulSoup

UrlMinfin = 'https://finance.i.ua/'
UrlGoogle = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&oq=%D0%BA%D1%83%D1%80%D1%81&aqs=chrome.1.69i57j0i131i433i512j0i433i512j0i131i433i512j0i512j69i61l3.4513j0j7&sourceid=chrome&ie=UTF-8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}


def parse_curs(URL, tipeTag, classTag):
    full_page = requests.get(URL, headers=headers)  # отримуємо весь код сторінки
    soup = BeautifulSoup(full_page.content, 'html.parser')  # парсимо код сторінки
    convert_rate = soup.findAll(tipeTag, class_=classTag)   # знаходимо всі елементи з вказаними атрибутами
    print(convert_rate) # виводимо всі елементи з вказаними атрибутами
    txt = convert_rate[0].text  # витягуємо з тега значення тексту
    curs = float(txt.replace(',', '.'))  # замінити в строці txt , на . та перевести в число
    return curs


def parse_curs_minfin(URL): #, tipeTag, classTag):
    full_page = requests.get(URL, headers=headers)  # отримуємо весь код сторінки
    soup = BeautifulSoup(full_page.content, 'html.parser')  # парсимо код сторінки
    # print(soup)
    # <td class="buy_rate"><span class="value "><span>31.5000</span></span></td>
    # <div class="widget widget-banks"
    # <div class="data_container">
    convert_rate = soup.findAll('div', class_='data_container')   # знаходимо всі елементи з вказаними атрибутами
    # print(convert_rate) # виводимо всі елементи з вказаними атрибутами
    convert_rate = convert_rate[0].findAll(True)
    # <td class="sell_rate"><span class="value "><span>31.8500</span></span></td>
    # print(convert_rate)
    # convert_rate = convert_rate.findAll('td')
    # # convert_rate = convert_rate[0].findAll('span')
    # print(convert_rate)
    for tag in convert_rate:
        tmp=tag.findAll('td')
        try:
            print(tmp[0].findAll('span'))
        except:
            pass
    # convert_rate = convert_rate[0].findAll('span', class_='mfm-posr')  # знаходимо всі елементи з вказаними атрибутами
    # print(convert_rate) # виводимо всі елементи з вказаними атрибутами
    txt = convert_rate[0].text  # витягуємо з тега значення тексту
    curs = float(txt.replace(',', '.'))  # замінити в строці txt , на . та перевести в число
    return curs

# # USD_GRN --> <span class="DFlfde SwHCTb" data-precision="2" data-value="29.56829">29,57</span>
# curs_ = parse_curs(UrlGoogle, 'span', 'DFlfde SwHCTb')
# print(curs_)

# <span class="mfm-posr">29.25490000</span>
# <td data-title="Продаж">
# <span class="mfm-posr">35.0000
# <span class="mfm-hover-show mfm-table-trend icon-up-open">+ 2.820</span>
# </span>
# </td>
curs_ = parse_curs_minfin(UrlMinfin)    #, 'span', 'mfm-posr')
print(curs_)
# save in file USD_GRN.txt
if curs_ > 0:
    with open('USD_GRN.txt', 'w') as f:
        f.write(str(datetime.datetime.now()) + '\n')
        # додати строку дати і часу запису в файл
        f.write(str(curs_))
        f.close()

# компилируємо файл в програму
#  pyinstaller -w ParsingCursDolaraGoogle.py
#  -w - запуск без виводу вікна консолі
#  -i "d:\шлях\файл іконки.ico" - додати іконку в програму
#  -F - компіляція в один файл
