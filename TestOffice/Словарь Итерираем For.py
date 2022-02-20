price = {'kay1': 1, 'kay2': 2, 'kay3': 0.5, 'kay4': 1.87}

for i in price:
    # print(i)  # в i помещаются ключи словаря
    price[i] = round(price[i] * 0.85, 2)  # сделаем скидку и округлим(round) до сотых
