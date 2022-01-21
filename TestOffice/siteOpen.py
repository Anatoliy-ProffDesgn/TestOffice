import os as s

# adr=input("Введите адрес сайта")
adr = "youtube.com"
if "https://" in adr:
    s.system('start ' + adr)
    print("if")

elif "www." in adr:
    adr = 'https://' + adr
    s.system('start ' + adr)
    print("efif")

else:
    adr = 'https://www.' + adr
    s.system('start ' + adr)
    print("else")
