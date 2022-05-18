p = 4.75
porc = [" порція коштує", " порції коштують", " порцій коштують"]
grn = [" гривня", " гривні", " гривень"]
kop = [" копійка", " копійки", " копійок"]

def pravylo(int_, list_):
    # якщо g закінчується на 1 окрім 11
    if int_ % 10 == 1 and int_ % 100 != 11:
        # тоді вивести слово "гривня"
        rez = str(int_) + list_[0]
    # якщо g закінчується на 2 - 4 окрім 12 - 14
    elif int_ % 10 in (2, 3, 4) and int_ % 100 not in (12, 13, 14):
        # тоді вивести слово "гривні"
        rez = str(int_) + list_[1]
    # якщо g закінчується на 0, 5 - 14
    else:
        # тоді вивести слово "гривень"
        rez = str(int_) + list_[2]
    return rez


for portion in range(1, 1022):
    price = portion * p
    prci = pravylo(portion, porc)
    grvn = pravylo(int(price), grn)
    kopi = pravylo(int(price * 100) % 100, kop)
    print(prci, grvn, kopi)