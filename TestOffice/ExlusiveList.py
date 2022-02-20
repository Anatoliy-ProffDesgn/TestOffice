def Exlusive_list(*args, sort=False):
    new_list = []
    for i in args:
        for j in i:
            if j not in new_list:
                new_list.append(j)
    if sort:
        new_list.sort()
    return new_list


a = [1, 2, 3, 8, 4, 9]
b = [8, 8, 4, 6, 7]
c = [1, 6, 8, 7, 9, 1]
z = Exlusive_list(a, b, c, sort=True)
print(z)
