import Price_Window as Pw
from PyQt5 import QtCore, QtGui, QtWidgets
from Open_Price import open_price


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

# -----------Створюємо модель даних і встановлюємо її в treeView---------
    ui.model = QtGui.QStandardItemModel()
    ui.treeView.setModel(ui.model)
    ui.treeView.setAlternatingRowColors(True)  # чергування кольру рядків

# -----------Встановлюємо заголовки стовпців-----------------------------
    ui.model.setHorizontalHeaderLabels(['Артикул', 'Назва виробу', 'Ціна', 'Одиниці', 'Категорія'])
    header = ui.treeView.header()
    header.resizeSection(0, 80)
    header.resizeSection(1, 550)
    header.resizeSection(2, 60)
    header.resizeSection(3, 60)

# -----------вмикаємо підтримку сортування----------------------------------
    ui.sortModel = CustomSortModel()
    ui.sortModel.setSourceModel(ui.model)
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
    data = open_price()
    def setData(data_rez):
        for item in data_rez:
            root = ui.model.invisibleRootItem()
            root.appendRow([QtGui.QStandardItem(item['Article']),
                            QtGui.QStandardItem(item['Name']),
                            QtGui.QStandardItem(item['Price']),
                            QtGui.QStandardItem(item['Unit']),
                            QtGui.QStandardItem(item['Category'])])
            par = root.child(root.rowCount() - 1)
            # print(root.rowCount(), par)




    # print(ui.treeView.model().rowCount())
    setData(data)
    ui.retranslateUi(Form)
    QtCore.QMetaObject.connectSlotsByName(Form)
    r = 'Кількість знайдених результатів: ' + str(len(data))
    ui.label.setText(r)  #'Кількість знайдених результатів' + len(data)


    def retranslateUi(Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


    Form.show()
    sys.exit(app.exec_())
