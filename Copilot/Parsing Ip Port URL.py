import os
import re

# import pandas as pd
'''get text from file'''
def open_file():
    '''open file this file is in the same directory'''
    file = os.path.dirname(os.path.abspath(__file__)) + '/text.txt'
    with open(file, 'r') as f:
        text = f.read()
    return text

def split_text(text):
    '''split text into strings'''
    tmp = text.split('\n')
    return tmp

def remove_empty(text):
    '''remove empty strings in array'''
    tmp = list(filter(None, text))
    return tmp

def filter_urls(text):
    '''filter urls in list'''
    tmp = list(filter(lambda x: re.match(r'https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', x), text))
    return tmp

def filter_not_urls(text):
    '''filter not urls in list'''
    tmp = list(filter(lambda x: not re.match(r'https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', x), text))
    return tmp

def find_ip(text):
    '''find ip in string'''
    tmp = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', text)
    return tmp

def remove_ip(text):
    '''remove ip in string'''
    tmp = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '', text)
    tmp = tmp.split(' ')
    tmp = remove_empty(tmp)
    for i in tmp:
        '''replace all spaces with '''
        t = i.replace(' ', '')
        '''replace / to " "'''
        t = t.replace('/', ' ')
        '''remove all signs except numbers and letters and spaces'''
        t = re.sub(r'[^\w\s]', '', t)
        t=t.split(' ')
        tmp[tmp.index(i)] = t
    return tmp


text = open_file()
text = split_text(text)
print(text)
text = remove_empty(text)
# print(text)
url = filter_urls(text)
print(url)
ip_port_method_str = filter_not_urls(text)
print(ip_port_method_str)

for i in ip_port_method_str:
    ip = find_ip(i)
    tmp= remove_ip(i)
    print(ip,tmp)
'''parsing ip and/or port and/or url in text'''
# def parse_text(text):
#     '''parsing ip'''
#     ip_pattern=re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
#     ip_list=re.findall(ip_pattern,text)
#     '''parsing port'''
#     port_pattern=re.compile(r'\d{1,5}')
#     port_list=re.findall(port_pattern,text)
#     '''parsing url'''
#     url_pattern=re.compile(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
#     url_list=re.findall(url_pattern,text)
#     return ip_list,port_list,url_list
# print(parse_text(text))
