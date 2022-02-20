price = {'key1': 1, 'key2': 2, 'key3': 0.5, 'key4': 1.87}

new_price = {}
for i in price:
    # print(i)  # в i помещаются ключи словаря
    new_price[i] = round(price[i] * 0.85, 2)  # сделаем скидку и округлим(round) до сотых
print(new_price)

for i in price.items():
    print(i)

new = {}
i = price.items()
print(i)
print(list(i))
for key, value in price.items():
    print(key, value)
    new[value] = key  # реверс словаря (ключ <=> значение) (поменяли местами)
print(new)

k = price.keys()
print(k)
v = price.values()
print(v)
print(list(v))
for v in price.values():
    print(v)

for i in price.keys():  # тот же цыкл что и в начале но с экономией памяти (вычисл. мощностей)
    # print(i)  # в i помещаются ключи словаря
    new_price[i] = round(price[i] * 0.85, 2)  # сделаем скидку и округлим(round) до сотых
print(new_price)
