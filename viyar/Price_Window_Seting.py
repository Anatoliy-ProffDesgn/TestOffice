import Price_Window as Pw
from PyQt5 import QtCore, QtGui, QtWidgets
from Open_Price import open_price

# list = Pw.Ui_Form().treeView()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Pw.Ui_Form()
    ui.setupUi(Form)

    # Створюємо модель даних і встановлюємо її в treeView
    ui.model = QtGui.QStandardItemModel()
    ui.treeView.setModel(ui.model)

    # Заповнюємо модель даних елементами з масиву
    data = open_price()
    for item in data:
        root = ui.model.invisibleRootItem()
        # print(item)
        root.appendRow([QtGui.QStandardItem(item['Article']),
                        QtGui.QStandardItem(item['Name']),
                        QtGui.QStandardItem(item['Price']),
                        QtGui.QStandardItem(item['Unit']),
                        QtGui.QStandardItem(item['Category'])])
        par = root.child(root.rowCount() - 1)
        # for art, name, prise, unit, catg in range(item['Article'], item['Name'], item['Price'], item['Unit'], item['Category']):
        #     #     for key, value in item.items():

    ui.retranslateUi(Form)
    QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    Form.show()
    sys.exit(app.exec_())

