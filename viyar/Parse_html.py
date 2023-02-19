# створено спираючись на інструкцію із https://python-scripts.com/beautifulsoup-html-parsing

# import requests
# from PyInstaller.isolated._parent import child
from bs4 import BeautifulSoup

f_name = './temp/newPrice1.html'


def Price_pars(file_name, e_cod='utf-8'):
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
            tmp.pop(), tmp.pop(0)
            price_val = tmp[len(tmp) - 2].split()
            tmp[len(tmp) - 2] = float(price_val[0].replace(',', '.'))
            tmp[len(tmp) - 1] = price_val[1] + '/' + tmp[len(tmp) - 1]
            rez.append(tmp)
    return {pr_title: rez}

rez=Price_pars(f_name)
# print(rez.keys())
# print(rez.items())
# print(rez.values())
# print(rez.popitem())
print(rez.values())
d_lst=list(rez.values())[0]
for lst in d_lst:
    print(lst)
print(rez.keys(), '\n' + str(len(d_lst)), '- строк(а)')
