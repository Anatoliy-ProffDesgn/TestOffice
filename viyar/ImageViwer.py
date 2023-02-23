import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


url = "https://example.com/image.jpg"
response = requests.get(url)
pixmap = QPixmap()
pixmap.loadFromData(response.content)
label.setPixmap(pixmap)