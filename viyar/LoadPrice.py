# Отримуємо данні з файлу temp/price.csv
from csv import reader as csv_reader
# fAdrRu = 'temp/price.csv' # https://viyar.ua/excel_export/?id=1981&lang=ru
# fAdrUa='temp/priceUA.csv' # https://viyar.ua/excel_export/?id=2521&lang=ua


def Read_CSV_FilePrice(f_Adr = 'temp/price.csv'):
    with open(f_Adr, 'r', encoding="UTF-8") as f:
        data = list(csv_reader(f))
    return data


# print((Read_CSV_FilePrice()))
