import Price_Window as Pw
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeView, QLineEdit
from Open_Price import open_price
from Search_txt_in_price import find_txt_in_price


class CustomSortModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left, right):
        if left.column() == right.column() == 2 or left.column() == right.column() == 0:  # Якщо це колонка з ціною (індекс 2)
            left_data = float(left.data())
            right_data = float(right.data())
            return left_data < right_data
        else:
            return super().lessThan(left, right)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Pw.Ui_Form()
    ui.setupUi(Form)

    # -----------Створюємо модель даних і встановлюємо її в treeView-------------------------------------------
    ui.model = QtGui.QStandardItemModel()
    ui.treeView.setModel(ui.model)
    ui.treeView.setAlternatingRowColors(True)  # чергування кольру рядків


    # -----------вмикаємо підтримку сортування--------------------------------------------------------------------
    def me_sort_mod(me_model):
        ui.sortModel = CustomSortModel()
        ui.sortModel.setSourceModel(me_model)
        ui.treeView.setModel(ui.sortModel)
        ui.treeView.setSortingEnabled(True)


    # -----------встановлюємо індекс колонки, по якій будуть сортуватися дані-------------------------------------
    # ui.treeView.setSortingColumn(0)

    def interior(me_model):
        # -----------Встановлюємо заголовки стовпців---------------------------------------------------------------
        me_model.setHorizontalHeaderLabels(['Артикул', 'Назва виробу', 'Ціна', 'Одиниці', 'Категорія'])
        header = ui.treeView.header()
        header.resizeSection(0, 80)
        header.resizeSection(1, 550)
        header.resizeSection(2, 60)
        header.resizeSection(3, 60)

        # -----------встановлюємо іконку для заголовка колонки--------------------------------------------------------
        header = ui.treeView.header()
        header.setSortIndicator(0, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(1, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(2, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(3, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(4, QtCore.Qt.AscendingOrder)


    # -----------Заповнюємо модель даних елементами з масиву------------------------------------------------------
    def setData(data_rez):
        interior(ui.model)
        ui.model.invisibleRootItem().clearData()
        for item in data_rez:
            root = ui.model.invisibleRootItem()
            root.appendRow([QtGui.QStandardItem(item['Article']),
                            QtGui.QStandardItem(item['Name']),
                            QtGui.QStandardItem(item['Price']),
                            QtGui.QStandardItem(item['Unit']),
                            QtGui.QStandardItem(item['Category'])])
        ui.treeView.setModel(ui.model)
        ui.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        # me_sort_mod(ui.model)
        ui.treeView.setSortingEnabled(True)


    # -----------------функція пошуку по назві-----------------------------------------------------
    def find_in():
        txt = ui.lineEdit_SearchName.text()
        if len(txt) > 0:
            data_2 = find_txt_in_price(txt, data, 'Name')
        else:
            data_2 = data

        if len(data_2) != len_dada or len(txt) != 0:
            ui.model2 = QStandardItemModel()
            interior(ui.model2)
            for item in data_2:
                ui.model2.appendRow([QtGui.QStandardItem(item['Article']),
                                     QtGui.QStandardItem(item['Name']),
                                     QtGui.QStandardItem(item['Price']),
                                     QtGui.QStandardItem(item['Unit']),
                                     QtGui.QStandardItem(item['Category'])])
            # встановити нову модель у treeView
            ui.treeView.setModel(ui.model2)
            row_count = ui.model2.rowCount()
            ui.label.setText(f"Кількість знайдених результатів: {row_count}")
            # відобразити модель
            ui.treeView.show()


    # -----------------Метод для обробки clicked на елементі treeView-----------------------------------
    def treeView_clicked(index):
        print(f"Клікнуто на елементі: рядок - {index.row()}, колонка - {index.column()}")


    # ----------------Метод для обробки подвійного doubleClicked на елементі treeView-----------------
    def treeView_doubleClicked(index):
        print(f"Подвійний клік на елементі: рядок - {index.row()}, колонка - {index.column()}")


    # ----------------Метод для обробки подвійного Clicked на елементі treeView.Header-----------------
    def handleHeaderClick(index):
        print(f'Header clicked: column {index}')
        me_sort_mod(ui.model)


    # ----------------Метод для обробки подвійного doubleClicked на елементі treeView.Header-----------------
    def handleHeaderDoubleClick(index):
        print(f'Header double clicked: column {index}')


    tmp = []
    data = open_price()
    len_dada = len(data)
    setData(data)
    r = str(ui.treeView.model().rowCount())
    ui.label.setText('Кількість знайдених результатів: ' + r)
    header = ui.treeView.header()

    # --------------------Підключення сигналів-------------------------------------------------------------
    ui.lineEdit_SearchName.textChanged.connect(find_in)
    ui.treeView.clicked.connect(treeView_clicked)
    ui.treeView.doubleClicked.connect(treeView_doubleClicked)
    header.sectionClicked.connect(handleHeaderClick)
    header.sectionDoubleClicked.connect(handleHeaderDoubleClick)


    def retranslateUi(Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


    Form.show()
    sys.exit(app.exec_())
