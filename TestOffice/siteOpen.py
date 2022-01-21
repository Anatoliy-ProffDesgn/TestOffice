from os import system as s_
import time
#from time import sleep as slp_
# adr=input("Введите адрес сайта")
adr = "youtube.com"
time.sleep(2) # пауза 2 секунды
if "https://" in adr:
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
