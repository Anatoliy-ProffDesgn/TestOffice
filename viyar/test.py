from Show_ImageViwer import *
# from ImageViwer import *

# import sys

# app = QtWidgets.QApplication(sys.argv)
# Form = QtWidgets.QWidget()
# ui = Ui_Form()
# ui.setupUi(Form)

update_image(ui.lineEdit_art.text())
ui.horizontalScrollBar.valueChanged.connect(slider_change)

Form.show()
sys.exit(app.exec_())
