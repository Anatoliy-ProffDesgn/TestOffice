from LoadURL import FileUrl_Load as load_file_in_url
import concurrent.futures


# ------------загрузка файлов із сайту---------------------
# адреси для загрузкі прайсів беремо з URL_list
# def download_price(urls):
#     i = int(0)
#     for url in urls:
#         i += 1
#         print(i, 'із', len(urls), 'Очікуєм')
#         try:
#             load_file_in_url(url, 'newPrice' + str(i) + '.html')
#         except Exception:
#             print('Помилка завантаження URL:', url)
#             continue
#         print('newPrice' + str(i) + '.xls', ' - Завантажено')


def download_price(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(load_file_in_url, url, f"newPrice{i}.html"): url for i, url in
                         enumerate(urls, 1)}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                print(f'Помилка завантаження URL {url}: {exc}')
            else:
                print(f'Файл для {url} успішно завантажено')
