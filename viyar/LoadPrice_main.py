from LoadURL import FileUrl_Load as load_file_in_url


# ------------загрузка файлов із сайту---------------------
# адреси для загрузкі прайсів беремо з URL_list
def download_price(urls):
    i = int(0)
    for url in urls:
        i += 1
        print(i, 'із', len(urls), 'Очікуєм')
        load_file_in_url(url, 'newPrice' + str(i) + '.html')
        print('newPrice' + str(i) + '.xls', ' - Завантажено')

