for i in range(3):                  # цикл ( повторення)
    a = input('введите float(): ')  # введення тексту
    b = float(a)                    # перетворення числа в дробове
    c = int(b)                      # перетворення числа в ціле
    print('a', type(a), '=', a)     # виведення данних на екран
    print('b', type(b), '=', b)     # виведення данних на екран
    print('c', type(c), '=', c)     # виведення данних на екран

for i in 'sssss':
    print(i)

for a in range(3, 6):
    print(type(a), a)

print(round(0.98 * 0.85, 2))  # округление до сотых