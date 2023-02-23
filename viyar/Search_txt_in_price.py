

def find_txt_in_price(txt, list_price, key):
    tmp = []
    l_txt = txt.split(' ')
    for item in list_price:
        search_str = str(item[key]).lower()
        inf = True
        for item_txt in l_txt:
            if not str(item_txt).lower() in search_str:
                inf = False
                break
        if inf:
            tmp.append(item)
    return tmp
