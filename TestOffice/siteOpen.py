from os import system as s_
import time

# from time import sleep as slp_
while True:
    adr = input("Введите адрес сайта\n")
    # adr = "youtube.com"
    time.sleep(2)  # пауза 2 секунды
    if adr == 'q' or adr == 'exit' or adr == 'quit':
        print('Proces EXIT')
        break
    elif "https://" in adr:
        s_('start ' + adr)
        print("if")
    elif "www." in adr:
        adr = 'https://' + adr
        s_('start ' + adr)
        print("efif")
    else:
        adr = 'https://www.' + adr
        s_('start ' + adr)
        print("else")
