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


tmp = []
data = open_price()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Pw.Ui_Form()
    ui.setupUi(Form)

    # -----------Створюємо модель даних і встановлюємо її в treeView---------
    ui.model = QtGui.QStandardItemModel()
    ui.treeView.setModel(ui.model)
    ui.treeView.setAlternatingRowColors(True)  # чергування кольру рядків
    def interior(me_model):
        # -----------Встановлюємо заголовки стовпців-----------------------------
        me_model.setHorizontalHeaderLabels(['Артикул', 'Назва виробу', 'Ціна', 'Одиниці', 'Категорія'])
        header = ui.treeView.header()
        header.resizeSection(0, 80)
        header.resizeSection(1, 550)
        header.resizeSection(2, 60)
        header.resizeSection(3, 60)

        # -----------вмикаємо підтримку сортування----------------------------------
        ui.sortModel = CustomSortModel()
        ui.sortModel.setSourceModel(me_model)
        ui.treeView.setModel(ui.sortModel)
        ui.treeView.setSortingEnabled(True)

        # -----------встановлюємо індекс колонки, по якій будуть сортуватися дані---
        # ui.treeView.setSortingColumn(0)

        # -----------встановлюємо іконку для заголовка колонки----------------------
        header = ui.treeView.header()
        header.setSortIndicator(0, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(1, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(2, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(3, QtCore.Qt.AscendingOrder)
        header.setSortIndicator(4, QtCore.Qt.AscendingOrder)


    # -----------Заповнюємо модель даних елементами з масиву--------------------
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


    setData(data)
    r = str(ui.treeView.model().rowCount())
    ui.label.setText('Кількість знайдених результатів: ' + r)

    # -----------------пошук по назві------------------------
    srch = ui.lineEdit_SearchName


    # -----------------функція пошуку по назві------------------------
    # def on_text_changed():
    #     txt = srch.text()
    #     print(txt)
    def find_in():
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

        # відобразити модель
        ui.treeView.show()


    data_2 = [{'Article': '131772', 'Name': 'Демпфер врізний Ø5мм BI-MATERIALE, білий, Italiana Ferramenta (23203010AB)',
              'Price': '1.5', 'Unit': 'грн/шт', 'Category': 'Амортизатори для дверей'},
             {'Article': '131781', 'Name': 'Демпфер врізний  Ø5мм K Flex L3мм, світл.сірий, Italiana Ferramenta (23203140IJ)',
              'Price': '3.06','Unit': 'грн/шт','Category': 'Амортизатори для дверей'},
             {'Article': '131773', 'Name': 'Демпфер врізний Ø5мм BI-MATERIALE, сірий, Italiana Ferramenta (23203010IF)',
              'Price': '1.5', 'Unit': 'грн/шт', 'Category': 'Амортизатори для дверей'},
             {'Article': '131774', 'Name': 'Демпфер врізний Ø5мм BI-MATERIALE, коричневий, Italiana Ferramenta (23203010MB)',
              'Price': '1.5', 'Unit': 'грн/шт', 'Category': 'Амортизатори для дверей'},
             {'Article': '131775', 'Name': 'Демпфер врізний Ø5мм BI-MATERIALE, прозорий, Italiana Ferramenta (23203010ZZ)',
              'Price': '1.5', 'Unit': 'грн/шт', 'Category': 'Амортизатори для дверей'}]

    ui.lineEdit_SearchName.textChanged.connect(find_in)
    layout = QVBoxLayout()
    # layout.addWidget(ui.search_box)
    # layout.addWidget(ui.tree_view)

    srch.setLayout(layout)




    # def on_rows_inserted(self, parent, start, end):
    #     # Отримуємо кількість рядків
    #     row_count = self.model.rowCount()
    #
    #     # Оновлюємо текст у QLabel
    #     # self.row_count_label.setText(f"Rows count: {row_count}")
    #     ui.label.setText(f"Кількість знайдених результатів: {row_count}")
    #
    #
    # # Підключаємо сигнал rowsInserted до слоту, що реагує на зміну кількості рядків
    # ui.model.rowsInserted.connect(on_rows_inserted)


    def retranslateUi(Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


    Form.show()
    sys.exit(app.exec_())
