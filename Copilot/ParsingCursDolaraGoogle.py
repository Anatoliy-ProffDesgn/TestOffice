import requests, datetime
from bs4 import BeautifulSoup


USD_GRN_URL = 'https://www.google.com/finance/quote/USD-UAH?sa=X&ved=2ahUKEwi_-uv3qPP3AhVNw4sKHcmlCXwQmY0JegQIDBAb'
USD_GRN = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&oq=%D0%BA%D1%83%D1%80%D1%81&aqs=chrome.1.69i57j0i131i433i512j0i433i512j0i131i433i512j0i512j69i61l3.4513j0j7&sourceid=chrome&ie=UTF-8'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}

full_page = requests.get(USD_GRN, headers=headers)
soup = BeautifulSoup(full_page.content, 'html.parser')

# USD_GRN --> <input class="lWzCpb a61j6" value="29.57" aria-label="Поле суми валюти" type="number" jsaction="input:trigger.Wtqxqe" data-ved="2ahUKEwi_-uv3qPP3AhVNw4sKHcmlCXwQwKsBegQIDBAK">
# USD_GRN --> <span class="DFlfde SwHCTb" data-precision="2" data-value="29.56829">29,57</span>
# convert_rate = soup.findAll('input', class_='lWzCpb a61j6')
convert_rate = soup.findAll('span', class_='DFlfde SwHCTb')

# USD_GRN_URL --> <div class="YMlKec fxKbKc">29,5683</div>
# convert_rate = soup.findAll('div', class_='YMlKec fxKbKc')

# print(convert_rate[0].text)
# save in file USD_GRN.txt
with open('USD_GRN.txt', 'w') as f:
    f.write(str(datetime.datetime.now()) + '\n')
    # додати строку дати і часу запису в файл
    f.write(convert_rate[0].text)
    f.close()

# компилируємо файл в програму
#  pyinstaller -w ParsingCursDolaraGoogle.py
    #  -w - запуск без виводу вікна консолі
    #  -i "d:\шлях\файл іконки.ico" - додати іконку в програму
    #  -F - компіляція в один файл
