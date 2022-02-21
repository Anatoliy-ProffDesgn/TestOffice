import os
import time

#
spisok = []
# s_Time = 24 * 60 * 60  # секунд в сутках
t = time.time()
for adr, dirs, files in os.walk('C:\\'):
    for file in files:
        fullNm = os.path.join(adr, file)  # адрес файла + имя (os.path.join() - расставляет сепараторы)
        spisok.append(fullNm)  # Добавить в список
t = time.time() - t
print(str(t) + 'c занял перебор адресов')
#         # Eсли  необходиво отобрать по дате созд.файла
#         # x_Time = time.time() - os.path.getctime(fullNm)
#         #     # time.time() - секунд от начала Эпохи до сейчас
#         #     # os.path.getctime(fullNm) - секунд от начала Эпохи до создания файла
#         # if ('.xls' in fullNm) and x_Time <= s_Time * 7:
#         #     spisok.append(fullNm) # Добавить в список
# # print(len(spisok), spisok)
#
# # 'r' открыть для чтения (по умолчанию)
# # 't' открыть в текстовом режиме (по умолчанию)
# # 'w' открыть для записи, содержимое файла удаляется, если файла нет, создается новый
# # 'a' открыть для дозаписо в конец файла, если файла нет, создается новый
# # 'b' открыть в бинарном режиме
# # '+' открыть для чтения и записи 'r+','w+', 'a+'

# r = open('text.txt', 'w')  # Открываем файл. Указываем полный путь к файлу если он не в директории програмы.
# r.write('Тест записи')  # записываем строку.
# r.close()  # Необходимо. После окончания работы закрываем файл.
#
# r = open('text.txt')  # Открываем файл для чтения.
# u = r.read()
# print(u)
# r.close()
no = 0
print(len(spisok))
r = open('text.txt', 'w')  # Открываем файл. Указываем полный путь к файлу если он не в директории програмы.
# r = open('text.txt', 'w', encoding='utf-8') # Если необходимо задать кодировку отличную от стандартной Windows
for i in spisok:
    try:
        r.write(i + '\n')  # записываем строку.
    except UnicodeEncodeError:
        no += 1
        print(no, 'UnicodeEncodeError', i)
r.close()  # Необходимо. После окончания работы закрываем файл.
