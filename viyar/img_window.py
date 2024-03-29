from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget


class MyLabel(QLabel):
    def __init__(self, pixmaps, index_label, parent=None):
        super().__init__(parent)

        self.pixmaps = pixmaps
        self.index = 0
        self.update_pixmap()
        self.index_label = index_label

    def update_pixmap(self):
        self.setPixmap(self.pixmaps[self.index])

    def show_previous_image(self):
        self.index = (self.index - 1) % len(self.pixmaps)
        self.update_pixmap()
        self.index_label.setText(f"{self.index + 1} із {len(self.pixmaps)} зображень")

    def show_next_image(self):
        self.index = (self.index + 1) % len(self.pixmaps)
        self.update_pixmap()
        self.index_label.setText(f"{self.index + 1} із {len(self.pixmaps)} зображень")

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
        self.setWindowTitle(self.name)
        self.setGeometry(100, 100, 400, 300)


        # Create buttons for navigating between images
        self.prev_button = QPushButton("<", self)
        self.next_button = QPushButton(">", self)
        self.next_button.setFocus()

        # Create a layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        # Create a label for the current index and total number of images
        self.index_label = QLabel(self)
        self.name_label = QLabel(self)
        self.label = MyLabel(self.pixmaps, self.index_label)
        # Create a label for the image and load the first pixmap
        self.label.setAlignment(Qt.AlignCenter)
        self.name_label.setText(self.name)

        self.update_index_label()
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.index_label)
        label_layout.addWidget(self.name_label)

        # Create a layout for the label and button layouts
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(button_layout)
        layout.addLayout(label_layout)

        # Create a main widget and set the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setModal(True)
        self.setLayout(layout)

        # Connect signals for the buttons
        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.next_button.setFocus()

        self.show()

    def show_previous_image(self):
        self.index = (self.index - 1) % len(self.pixmaps)
        self.label.setPixmap(self.pixmaps[self.index])
        self.update_index_label()

    def show_next_image(self):
        self.index = (self.index + 1) % len(self.pixmaps)
        self.label.setPixmap(self.pixmaps[self.index])
        self.update_index_label()

    def update_index_label(self):
        self.index_label.setText(f"{self.index + 1} із {len(self.pixmaps)} зображень")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.reject()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.show_previous_image()
        else:
            self.show()


def open_img_window(pixmaps):
    dialog = MyImageDialog(pixmaps)
    dialog.exec_()
