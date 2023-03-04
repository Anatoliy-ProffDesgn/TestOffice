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
        Form.resize(1205, 804)
        self.label_PriceDataName = QtWidgets.QLabel(Form)
        self.label_PriceDataName.setGeometry(QtCore.QRect(10, 0, 301, 16))
        self.label_PriceDataName.setObjectName("label_PriceDataName")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 1191, 781))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.treeView_2 = QtWidgets.QTreeView(self.gridLayoutWidget)
        self.treeView_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView_2.setObjectName("treeView_2")
        self.gridLayout.addWidget(self.treeView_2, 1, 0, 1, 1)
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
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)
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
        self.lineEdit_SearchCategori = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_SearchCategori.setObjectName("lineEdit_SearchCategori")
        self.gridLayout_2.addWidget(self.lineEdit_SearchCategori, 1, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 4)
        self.gridLayout_2.setColumnStretch(2, 2)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.treeView = QtWidgets.QTreeView(self.gridLayoutWidget)
        self.treeView.setBaseSize(QtCore.QSize(747, 455))
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 100)
        self.verticalLayout.setStretch(2, 5)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
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
        self.label_5.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_5.setWordWrap(False)
        self.label_5.setIndent(0)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.label_img = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_img.setEnabled(True)
        self.label_img.setAutoFillBackground(True)
        self.label_img.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_img.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_img.setText("")
        self.label_img.setObjectName("label_img")
        self.verticalLayout_2.addWidget(self.label_img)
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
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 5)
        self.verticalLayout_2.setStretch(2, 100)
        self.verticalLayout_2.setStretch(3, 5)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_Update = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_Update.setObjectName("pushButton_Update")
        self.gridLayout_3.addWidget(self.pushButton_Update, 4, 0, 1, 1)
        self.pushButton_SaveViyar = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_SaveViyar.setFont(font)
        self.pushButton_SaveViyar.setObjectName("pushButton_SaveViyar")
        self.gridLayout_3.addWidget(self.pushButton_SaveViyar, 6, 1, 1, 1)
        self.pushButton_Clear = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.gridLayout_3.addWidget(self.pushButton_Clear, 3, 0, 1, 1)
        self.pushButton_SaveCustom = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_SaveCustom.setObjectName("pushButton_SaveCustom")
        self.gridLayout_3.addWidget(self.pushButton_SaveCustom, 2, 0, 1, 1)
        self.pushButton_OpenViyar = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_OpenViyar.setObjectName("pushButton_OpenViyar")
        self.gridLayout_3.addWidget(self.pushButton_OpenViyar, 5, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.radioButton_All = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_All.setGeometry(QtCore.QRect(10, 20, 208, 17))
        self.radioButton_All.setObjectName("radioButton_All")
        self.radioButton_Custom = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_Custom.setGeometry(QtCore.QRect(10, 40, 208, 17))
        self.radioButton_Custom.setObjectName("radioButton_Custom")
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 3)
        self.gridLayout_3.setColumnStretch(1, 2)
        self.gridLayout_3.setRowStretch(2, 5)
        self.gridLayout_3.setRowStretch(3, 5)
        self.gridLayout_3.setRowStretch(4, 5)
        self.gridLayout_3.setRowStretch(5, 5)
        self.gridLayout_3.setRowStretch(6, 5)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 7)
        self.gridLayout.setColumnStretch(1, 4)
        self.gridLayout.setRowStretch(0, 7)
        self.gridLayout.setRowStretch(1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit_SearchName, self.treeView)
        Form.setTabOrder(self.treeView, self.treeView_2)
        Form.setTabOrder(self.treeView_2, self.pushButton_SaveViyar)
        Form.setTabOrder(self.pushButton_SaveViyar, self.pushButton_Update)
        Form.setTabOrder(self.pushButton_Update, self.lineEdit_SearchArt)
        Form.setTabOrder(self.lineEdit_SearchArt, self.lineEdit_SearchCategori)
        Form.setTabOrder(self.lineEdit_SearchCategori, self.pushButton_Clear)
        Form.setTabOrder(self.pushButton_Clear, self.pushButton_SaveCustom)
        Form.setTabOrder(self.pushButton_SaveCustom, self.pushButton_OpenViyar)
        Form.setTabOrder(self.pushButton_OpenViyar, self.radioButton_All)
        Form.setTabOrder(self.radioButton_All, self.radioButton_Custom)
        Form.setTabOrder(self.radioButton_Custom, self.pushButton)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Прайс"))
        self.label_PriceDataName.setText(_translate("Form", "TextLabel"))
        self.label_4.setText(_translate("Form", "Пошук за артикулом"))
        self.label_2.setText(_translate("Form", "Пошук за категорією"))
        self.label_3.setText(_translate("Form", "Пошук за назвою"))
        self.label.setText(_translate("Form", "кількість знайдених результатів"))
        self.label_5.setText(_translate("Form", "Завантажити на viyar.ua"))
        self.pushButton.setText(_translate("Form", "Завантажити на viyar.ua"))
        self.label_art.setText(_translate("Form", "TextLabel"))
        self.pushButton_Update.setText(_translate("Form", "Оновити прайси"))
        self.pushButton_SaveViyar.setText(_translate("Form", "Зберегти для Віяр"))
        self.pushButton_Clear.setText(_translate("Form", "Очистити обране"))
        self.pushButton_SaveCustom.setText(_translate("Form", " Зберегти обране як користувацький прайс "))
        self.pushButton_OpenViyar.setText(_translate("Form", "Завантажити файл Віяр"))
        self.groupBox.setTitle(_translate("Form", "Оберіть якім прайсом бажаєте користуватись"))
        self.radioButton_All.setText(_translate("Form", "Повний прайс"))
        self.radioButton_Custom.setText(_translate("Form", "Користувацький прайс"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
