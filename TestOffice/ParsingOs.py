import os
import time

spisok = []
s_Time = 24 * 60 * 60  # секунд в сутках

for adr, dirs, files in os.walk('D:\\OneDrive\RFlesh'):
    for file in files:
        fullNm = os.path.join(adr, file)    # адрес файла + имя (os.path.join() - расставляет сепараторы)
        x_Time = time.time() - os.path.getctime(fullNm)
        # time.time() - секунд от начала Эпохи до сейчас
        # os.path.getctime(fullNm) - секунд от начала Эпохи до создания файла
        if ('.xls' in fullNm) and x_Time <= s_Time * 7:
            spisok.append(fullNm)

print(len(spisok), spisok)
