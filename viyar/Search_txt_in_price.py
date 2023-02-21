def find_txt_in_price(txt, list_price, key):
    tmp = []
    if len(txt) > 2:
        for item in list_price:
            if txt in item[key]:
                print(txt)
                tmp.append(item)
    else:
        tmp = False
    print(type(tmp))
    return tmp
