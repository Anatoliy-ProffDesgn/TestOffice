age = int(input('Введіть вік людини '))
s = input('Стать (m/w)')
rez = [['Дошкільня', 'Дошкільня'], ['Школяр', 'Школярка'], ['Дорослий', 'Доросла'], ['Пенсіонер', 'Пенсіонерка']]
if s == 'm':
    s = 0
elif s == 'w':
    s = 1
else:
    print("Стать указано невірно")
    exit()

if age > 0 and age < 5:
    a = 0
elif age > 5 and age < 19:
    a = 1
elif age > 18 and age < 60:
    a = 2
else:
    a = 3

print(rez[a][s])
