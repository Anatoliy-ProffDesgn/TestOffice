from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QScrollArea
class MyLabel(QLabel):
    def __init__(self, pixmaps, parent=None):
        super().__init__(parent)

        self.pixmaps = pixmaps
        self.index = 0
        self.update_pixmap()

    def update_pixmap(self):
        self.setPixmap(self.pixmaps[self.index])

    def show_previous_image(self):
        self.index = (self.index - 1) % len(self.pixmaps)
        self.update_pixmap()

    def show_next_image(self):
        self.index = (self.index + 1) % len(self.pixmaps)
        self.update_pixmap()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.show_previous_image()
        else:
            self.show_next_image()

class MyImageDialog(QDialog):
    def __init__(self, pixmaps, name):
        super().__init__()
        self.pixmaps = pixmaps
        self.index = 0
        self.current_pixmap_index = 0
        self.name = name
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.name)
        self.setGeometry(100, 100, 400, 300)

        # Create a label for the image and load the first pixmap
        self.label = MyLabel(self.pixmaps)
        # self.label.setPixmap(self.pixmaps[self.index])
        self.label.setAlignment(Qt.AlignCenter)


        # Create a label for the image and load the first pixmap

        # Create buttons for navigating between images
        self.prev_button = QPushButton("<", self)
        self.next_button = QPushButton(">", self)
        self.next_button.setFocus()

        # Create a layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        # Create a layout for the label and button layouts
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(button_layout)

        # Create a label for the current index and total number of images
        self.index_label = QLabel(self)
        self.update_index_label()
        layout.addWidget(self.index_label)

        # Create a main widget and set the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setModal(True)
        self.setLayout(layout)

        # Connect signals for the buttons
        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.next_button.setFocus()


        # self.scroll = QScrollArea()
        # self.scroll.setWidget(self.label)
        # # Встановлення зв'язків між подіями та обробником подій
        # self.scroll.verticalScrollBar().valueChanged.connect(self.on_scroll)
        # self.label.mouseReleaseEvent = self.on_mouse_release

        self.show()

    def on_scroll(self, event):
        if event.orientation() == Qt.Vertical:
            if event.angleDelta().y() > 0:
                self.show_previous_image()
            else:
                self.show_next_image()

    def on_mouse_release(self, event):
        if event.button() == Qt.LeftButton:
            if event.pos().x() < self.label.width() / 2:
                self.show_previous_image()
            else:
                self.show_next_image()

    def show_previous_image(self):
        self.index = (self.index - 1) % len(self.pixmaps)
        self.label.setPixmap(self.pixmaps[self.index])
        self.update_index_label()

    def show_next_image(self):
        self.index = (self.index + 1) % len(self.pixmaps)
        self.label.setPixmap(self.pixmaps[self.index])
        self.update_index_label()

    def update_index_label(self):
        self.index_label.setText(f"{self.index+1} із {len(self.pixmaps)} зображень")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.reject()
        elif event.key() == Qt.Key_Up:
            self.show_next_image()
        elif event.key() == Qt.Key_Down:
            self.show_previous_image()

    # def wheelEvent(self, event):
        # Increase or decrease zoom level based on direction of scroll
        # self.zoom_level += 1 if event.angleDelta().y() > 0 else -1
        # self.zoom_level = max(-5, min(self.zoom_level, 5))
        # if self.zoom_level != 0:
        #     # Scale the pixmap based on the zoom level
        #     pixmap = self.pixmaps[self.index]
        #     scaled_size = pixmap.size() * (1 + self.zoom_level * 0.1)
        #     pixmap = pixmap.scaled(scaled_size.toSize(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        #     self.label.setPixmap(pixmap)
        # else:
        #     # Reset the pixmap to the original size
        #     self.label.setPixmap(self.pixmaps[self.index])

def open_img_window(pixmaps):
    dialog = MyImageDialog(pixmaps)
    dialog.exec_()
