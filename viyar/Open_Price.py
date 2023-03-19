import json as js
import os

import AllFile_inDir as All_files


# ---------------Open json------------------
def open_price(file_name=''):
    if file_name == '':
        file_name = All_files.get_file('./Price')
        file = [new_file(file_name)]
    else:
        file = [file_name]
    with open(file[0], 'r', encoding='utf-8') as f:
        price = js.load(f)
    prices = [price, file]
    return prices


def open_custom_price(file_name='Custom/customPrice.json'):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            custom_price = js.load(f)
    except:
        pass
    return custom_price


def new_file(files):
    latest_file = None
    latest_modification_time = 0

    for file_path in files:
        modification_time = os.path.getmtime(file_path)
        if modification_time > latest_modification_time:
            latest_file = file_path
            latest_modification_time = modification_time

    # print(latest_file)
    return latest_file


# ---------------test------------------
if __name__ == "__main__":
    i = 0
    j = 0
    for p in open_price():
        i += 1
        search_str = 'зав'
        if (search_str.lower() in str(p['Name']).lower()) or (search_str.lower() in str(p['Category']).lower()):
            j += 1
            print(i, p)
    print('Знайдено', j)
