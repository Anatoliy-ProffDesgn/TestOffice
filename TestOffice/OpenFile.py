import os

spisok = []
# # 'r' открыть для чтения (по умолчанию)
# # 't' открыть в текстовом режиме (по умолчанию)
# # 'w' открыть для записи, содержимое файла удаляется, если файла нет, создается новый
# # 'a' открыть для дозаписо в конец файла, если файла нет, создается новый
# # 'b' открыть в бинарном режиме
# # '+' открыть для чтения и записи 'r+','w+', 'a+'
no = 0
_vid = ['.mp4', '.avi', '.mkv', '.wmv', '.flv', '.mpeg', '.mpg', '.m4v', '.mov', '.3gp2', '.3gp', '.3g2']
_iskl = ['Movavi', 'ViberDownloads','amd64_microsoft','SystemSettings','Package_for_Rollup','мебель видео','Рабочий стол\DCIM','AppData\Roaming\Adobe']
MeFile = open('text.txt', 'r')  # Открываем файл. Указываем полный путь к файлу если он не в директории програмы.
# MeFile = open('text.txt', 'r', encoding='utf-8') # Если необходимо задать кодировку отличную от стандартной Windows
for MeString in MeFile:
    for vid in _vid:
        f=False
        for iskl in _iskl:
            if iskl in MeString:
                f=True
                break
        if f: continue
        if vid in MeString:
            spisok.append(MeString)  # записываем строку.
MeFile.close()  # Необходимо. После окончания работы закрываем файл.

for i in spisok:
    print(i)

print(len(spisok))