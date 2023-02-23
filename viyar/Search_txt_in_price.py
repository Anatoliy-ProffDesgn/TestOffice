def find_txt_in_price(txt, list_price, key):
    tmp = []
    tmp2 = []
    l_txt = find_list(txt)
    # if len(l_txt) == 0:
    #     tmp = list_price
    for item in list_price:
        search_str = str(item[key]).lower()
        inf = True
        for item_txt in l_txt:
            if not str(item_txt).lower() in search_str:
                inf = False
                break
        if inf:
            tmp.append(item)

    l_txt = find_del_list(txt)
    # if len(l_txt) == 0:
    #     tmp2 = tmp
    for item in tmp:
        search_str = str(item[key]).lower()
        inf = True
        for item_txt in l_txt:
            if item_txt in search_str:
                inf = False
                break
        if inf:
            tmp2.append(item)

    return tmp2


def find_del_list(txt):
    f_list = txt.split(' ')
    tmp = []
    for item in f_list:
        if len(item) > 0:
            if item[0] == '-':
                tmp.append(item[1:])
    for item in tmp:
        if len(item) < 3:
            tmp.remove(item)
    return tmp


def find_list(txt):
    f_list = txt.split(' ')
    tmp = []
    for item in f_list:
        if len(item) > 0:
            if not item[0] == '-':
                tmp.append(item)
    for item in tmp:
        if len(item) < 3:
            tmp.remove(item)
    return tmp


# print(find_list("петл накл про -пол -бе -каол"))
