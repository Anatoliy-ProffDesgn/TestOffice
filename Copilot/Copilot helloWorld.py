import os
import re
'''get text from file'''

'''open file this file is in the same directory'''
def open_file():
    file=os.path.dirname(os.path.abspath(__file__))+'/text.txt'
    with open(file,'r') as f:
        text=f.read()
    return text
print(open_file())
'''parsing ip and/or port and/or url in text'''
def parse(text):
    ip=re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',text)
    port=re.findall(r'\d{1,5}',text)
    url=re.findall(r'(http|https)://[a-zA-Z0-9\./]+',text)
    return ip,port,url
print(parse(text))