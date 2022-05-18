d = 0
s = ""
ch = int(input("Введіть чисельник: "))
cn = int(input("Введіть знаменник: "))
print("Дріб:", str(ch) + "/" + str(cn))

for chyslo in range(min(ch, cn), 0, -1):
    if ch % chyslo == 0 and cn % chyslo == 0:
        # print(chyslo)
        d = chyslo
        break
ch = int(ch // d)
cn = int(cn // d)
print("Скорочений дріб:", str(ch) + "/" + str(cn))

if ch > cn:
    print("Дріб неправильний")
else:
    for i in range(1, cn + 1):
        if i <= ch:
            s += "x"
        else:
            s += "0"

    print("Дріб правильний")
    print("Зображення дробу:", s)