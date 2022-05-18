import re
from bs4 import BeautifulSoup
import requests

url = "https://kinoprofi.vip/"

html = requests.get(url)
soup = BeautifulSoup(html.content, 'lxml')
title = soup.title
print(title)

# '''parsing site url'''
# def parsing_url(url):
