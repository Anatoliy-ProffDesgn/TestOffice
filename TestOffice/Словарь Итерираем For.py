price = {'key1': 1, 'key2': 2, 'key3': 0.5, 'key4': 1.87}

new_price = {}
for i in price:
    # print(i)  # в i помещаются ключи словаря
    new_price[i] = round(price[i] * 0.85, 2)  # сделаем скидку и округлим(round) до сотых
print(new_price)

for i in price.items():
    print(i)

new = {}
for key, value in price.items():
    print(key, value)
    new[value] = key    # реверс словаря (ключ <=> значение) (поменяли местами)
print(new)
