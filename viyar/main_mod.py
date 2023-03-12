from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QStringListModel, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QHeaderView

import inet_test
from Price_Window import Ui_Form
from Open_Price import open_price
import Images as img

# -------------------Global-------------------------
global full_model
global custom_model
global old_model
global null_model
global save_model
global full_category
global custom_category
global label_width
global label_height
global pixmaps

class CustomSortModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left, right):
        # Сортувати як числа колонки (індекс 2 та 0)
        if left.column() == right.column() == 2 or left.column() == right.column() == 0:
            if left.data() and right.data():
                left_data = float(left.data())
                right_data = float(right.data())
                return left_data < right_data
            else:
                return False
        else:
            return super().lessThan(left, right)


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create an instance of the form
        self.ui = Ui_Form()

        # Call the setupUi method passing self as parent
        self.ui.setupUi(self)

        # Do other stuff here
        # Create a QStandardItemModel and set it as the model of the treeView
        self.model = QtGui.QStandardItemModel()
        self.ui.treeView.setModel(self.model)

        # Sort the data by the first column
        self.ui.treeView.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
        self.ui.treeView.header().setSortIndicatorShown(True)
        self.ui.treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)

        # Connect the context menu signal to a slot
        self.ui.treeView.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.treeView.doubleClicked.connect(self.on_tree_view_double_clicked)

        self.ui.horizontalScrollBar.valueChanged.connect(self.slider_move)
        # додатковий код для заповнення treeView
        # ...


        # -------------------Global-------------------------
        global full_model
        global custom_model
        global full_category
        global custom_category

        # -------------------мій функціонал-------------------------
        me_data = open_price()
        full_model = self.create_me_model(me_data[0])
        custom_model = self.create_me_model(me_data[2])
        full_category = self.create_category(me_data[0])
        custom_category = self.create_category(me_data[2])
        self.treeView_set_model(self.ui.treeView, full_model)
        self.combo_box_set_data()

    def on_tree_view_double_clicked(self, index: QModelIndex):
        print(f"Подвійний клік на елементі з індексом {index.row()}")
        art = self.ui.treeView.model().index(index.row(), 0).data()
        global pixmaps
        pixmaps = img.count_image(art)
        img.get_image(self.ui.label_img, pixmaps[0])
        self.ui.horizontalScrollBar.setMaximum(len(pixmaps))

    def slider_move(self):
        global pixmaps
        try:
            img.get_image(self.ui.label_img, pixmaps[self.ui.horizontalScrollBar.value()])
        except:
            pass

    def create_category(self, data):
        category = list(set([d['Category'] for d in data]))
        category.sort()
        return category

    def create_me_model(self, me_data):
        # Створення моделі
        me_model = QStandardItemModel()
        # Встановлення заголовків стовпців
        keys = ['Article', 'Name', 'Price', 'Unit', 'Category']
        header = ['Артикул', 'Назва', 'Ціна', 'Одиниці', 'Категорія']
        me_model.setHorizontalHeaderLabels(header)

        # Додавання даних до моделі
        for data in me_data:
            row = []
            for key in keys:
                item = QStandardItem(str(data.get(key, '')))
                row.append(item)
            me_model.appendRow(row)
        return me_model

    def treeView_set_model(self, tree_view, me_model):
        # -----------Встановлюємо заголовки стовпців---------------------------------------------------------------
        # self.clear_model(tree_view, tree_view.model())
        tree_view.setModel(me_model)
        header = tree_view.header()
        header.resizeSection(0, 80)
        header.resizeSection(1, 400)
        header.resizeSection(2, 60)
        header.resizeSection(3, 60)
        # -----------встановлюємо іконку для заголовка колонки-----------------------------------------------------
        header.setSortIndicator(0, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(1, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(2, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(3, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(4, QtCore.Qt.AscendingOrder)

        sort_model = CustomSortModel()
        sort_model.setSourceModel(me_model)
        tree_view.setModel(sort_model)
        tree_view.setSortingEnabled(True)

    def combo_box_set_data(self, data=''):
        if data == '':
            data = full_category
        model = QStringListModel()
        model.setStringList(data)
        # Додаємо список до комбінованого списку
        self.ui.comboBox.setModel(model)
        self.ui.comboBox.show()
        self.ui.comboBox.setCurrentIndex(-1)

    def show_context_menu(self, point):
        # Create a context menu
        self.context_menu = QtWidgets.QMenu(self)
        self.context_menu.addAction("Повний прайс", self.full_price_triggered)
        self.context_menu.addAction("Мій прайс", self.custom_price_triggered)
        # Show the context menu at the cursor's position
        self.context_menu.exec_(self.ui.treeView.mapToGlobal(point))



    def full_price_triggered(self):
        # Handle Повний прайс
        self.treeView_set_model(self.ui.treeView, full_model)
        self.combo_box_set_data()
        print("Action 1 triggered")

    def custom_price_triggered(self):
        # Handle action 2
        self.treeView_set_model(self.ui.treeView, custom_model)
        self.combo_box_set_data(custom_category)
        print("Action 2 triggered")



# Create the application and show the main window
app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
app.exec_()
