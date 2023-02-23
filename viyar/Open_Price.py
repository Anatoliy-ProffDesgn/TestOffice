import json as js
import AllFile_inDir as All_files


# ---------------Open json------------------
def open_price(file_name=''):
    if file_name == '':
        file_name = All_files.get_file('./Price')
        file_name = [str(file_name[len(file_name)-1])]
    else:
        file_name = [file_name]
    with open(file_name[0], 'r', encoding='utf-8') as f:
        price = js.load(f)
    return [price, file_name]

# ---------------test------------------
# i = 0
# j = 0
# for p in open_price():
#     i += 1
#     search_str = 'зав'
#     if (search_str.lower() in str(p['Name']).lower()) or (search_str.lower() in str(p['Category']).lower()):
#         j += 1
#         print(i, p)
# print('Знайдено', j)