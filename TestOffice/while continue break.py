x = ''  # h e l l o
while len(x) < 5:
    y = input('Ввод данных: ')
    if 'l' in y:
        print('l - запрещено, введите другое значение')
        continue        # пропустить итерацию
    if 'o' in y:
        print('о - цыкл прерван')
        break           # прервать цыкл
    x += y
else:
    print(x)
