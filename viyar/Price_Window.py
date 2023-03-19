# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Price_Window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(1204, 828)
        self.label_PriceDataName = QtWidgets.QLabel(Form)
        self.label_PriceDataName.setGeometry(QtCore.QRect(10, 0, 301, 16))
        self.label_PriceDataName.setObjectName("label_PriceDataName")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 1191, 801))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_img = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_img.setEnabled(True)
        self.label_img.setAutoFillBackground(True)
        self.label_img.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_img.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_img.setObjectName("label_img")
        self.verticalLayout_2.addWidget(self.label_img)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.radioButton_All = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_All.setGeometry(QtCore.QRect(10, 20, 208, 17))
        self.radioButton_All.setChecked(True)
        self.radioButton_All.setAutoExclusive(False)
        self.radioButton_All.setObjectName("radioButton_All")
        self.radioButton_Custom = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_Custom.setGeometry(QtCore.QRect(10, 40, 208, 17))
        self.radioButton_Custom.setObjectName("radioButton_Custom")
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.pushButton_Update = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_Update.setObjectName("pushButton_Update")
        self.gridLayout_3.addWidget(self.pushButton_Update, 4, 0, 1, 1)
        self.pushButton_SaveCustom = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_SaveCustom.setObjectName("pushButton_SaveCustom")
        self.gridLayout_3.addWidget(self.pushButton_SaveCustom, 2, 0, 1, 1)
        self.pushButton_Clear = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.gridLayout_3.addWidget(self.pushButton_Clear, 3, 0, 1, 1)
        self.pushButton_OpenViyar = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_OpenViyar.setObjectName("pushButton_OpenViyar")
        self.gridLayout_3.addWidget(self.pushButton_OpenViyar, 5, 0, 1, 1)
        self.pushButton_SaveViyar = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_SaveViyar.setFont(font)
        self.pushButton_SaveViyar.setObjectName("pushButton_SaveViyar")
        self.gridLayout_3.addWidget(self.pushButton_SaveViyar, 6, 0, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 3)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.gridLayoutWidget)
        self.horizontalScrollBar.setPageStep(1)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.horizontalLayout.addWidget(self.horizontalScrollBar)
        self.label_art = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_art.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_art.setAlignment(QtCore.Qt.AlignCenter)
        self.label_art.setObjectName("label_art")
        self.horizontalLayout.addWidget(self.label_art)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(0, 100)
        self.verticalLayout_2.setStretch(2, 5)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.lineEdit_SearchArt = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_SearchArt.setObjectName("lineEdit_SearchArt")
        self.gridLayout_2.addWidget(self.lineEdit_SearchArt, 1, 0, 1, 1)
        self.lineEdit_SearchName = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_SearchName.setObjectName("lineEdit_SearchName")
        self.gridLayout_2.addWidget(self.lineEdit_SearchName, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 4, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_2.addWidget(self.comboBox, 1, 4, 1, 1)
        self.lineEdit_max = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_max.setObjectName("lineEdit_max")
        self.gridLayout_2.addWidget(self.lineEdit_max, 1, 3, 1, 1)
        self.lineEdit_min = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_min.setObjectName("lineEdit_min")
        self.gridLayout_2.addWidget(self.lineEdit_min, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 3, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 5)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setColumnStretch(4, 3)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.treeView = QtWidgets.QTreeView(self.gridLayoutWidget)
        self.treeView.setBaseSize(QtCore.QSize(747, 455))
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_5.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(7)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setWordWrap(False)
        self.label_5.setIndent(0)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.treeView_2 = QtWidgets.QTreeView(self.gridLayoutWidget)
        self.treeView_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView_2.setObjectName("treeView_2")
        self.verticalLayout.addWidget(self.treeView_2)
        self.label_summ = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_summ.setFont(font)
        self.label_summ.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_summ.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_summ.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_summ.setObjectName("label_summ")
        self.verticalLayout.addWidget(self.label_summ)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 100)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 7)
        self.gridLayout.setRowStretch(0, 7)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit_SearchName, self.treeView)
        Form.setTabOrder(self.treeView, self.pushButton_Update)
        Form.setTabOrder(self.pushButton_Update, self.lineEdit_SearchArt)
        Form.setTabOrder(self.lineEdit_SearchArt, self.pushButton_Clear)
        Form.setTabOrder(self.pushButton_Clear, self.pushButton_SaveCustom)
        Form.setTabOrder(self.pushButton_SaveCustom, self.radioButton_All)
        Form.setTabOrder(self.radioButton_All, self.radioButton_Custom)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Прайс"))
        self.label_PriceDataName.setText(_translate("Form", "TextLabel"))
        self.label_img.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Подвійний клік по рядку фурнітури<br/>виведе її забраження з сайту віяр</span></p></body></html>"))
        self.groupBox.setTitle(_translate("Form", "Оберіть якім прайсом бажаєте користуватись"))
        self.radioButton_All.setText(_translate("Form", "Повний прайс"))
        self.radioButton_Custom.setText(_translate("Form", "Користувацький прайс"))
        self.pushButton_Update.setText(_translate("Form", "Оновити прайси"))
        self.pushButton_SaveCustom.setText(_translate("Form", " Зберегти обране як користувацький прайс "))
        self.pushButton_Clear.setText(_translate("Form", "Очистити обране"))
        self.pushButton_OpenViyar.setText(_translate("Form", "Завантажити файл Віяр"))
        self.pushButton_SaveViyar.setText(_translate("Form", "Зберегти для Віяр"))
        self.label_art.setText(_translate("Form", "TextLabel"))
        self.label_4.setText(_translate("Form", "Артикул"))
        self.label_3.setText(_translate("Form", "Пошук за назвою"))
        self.label_2.setText(_translate("Form", "Пошук за категорією"))
        self.lineEdit_max.setText(_translate("Form", "0"))
        self.lineEdit_min.setText(_translate("Form", "0"))
        self.label_6.setText(_translate("Form", "Ціна від"))
        self.label_7.setText(_translate("Form", "до"))
        self.label.setText(_translate("Form", "кількість знайдених результатів"))
        self.label_5.setText(_translate("Form", "Преглянути на сайті viyar.ua"))
        self.pushButton.setText(_translate("Form", "Завантажити з сайту viyar.ua"))
        self.label_summ.setText(_translate("Form", "Сума:_______"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
