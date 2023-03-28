import sqlite3

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QHeaderView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import sys
import pandas as pd
from PySide2.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Price list")
        self.setGeometry(100, 100, 800, 600)

        # Підключення до бази даних
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('DataBase.db')
        db.open()
        # З'єднання з базою даних
        self.conn = sqlite3.connect('DataBase.db')

        # Зчитування даних з бази даних
        self.df = pd.read_sql_query("SELECT * FROM price_26_03_2023", self.conn)

        # Створення QSqlTableModel для прайсу
        model = QSqlTableModel()
        model.setTable('price_26_03_2023')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()

        # Створення віджету таблиці та налаштування сортування
        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Перетворення pandas.DataFrame в pd_table_model
        pd_table_model = pd_table_model_from_dataframe(self.df)

        # Відображення даних у таблиці
        self.table.setModel(pd_table_model)

        # Налаштування віджетів у вікні
        central_widget = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)


def pd_table_model_from_dataframe(dataframe):
    """
    Функція для перетворення pandas.DataFrame в pd_table_model
    """
    class PandasModel(QAbstractTableModel):
        def __init__(self, data):
            QAbstractTableModel.__init__(self)
            self._data = data

        def rowCount(self, parent=None):
            return len(self._data.values)

        def columnCount(self, parent=None):
            return self._data.columns.size

        def data(self, index, role=Qt.DisplayRole):
            if index.isValid():
                if role == Qt.DisplayRole:
                    return str(self._data.values[index.row()][index.column()])
            return None

        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self._data.columns[col]
            return None

    return PandasModel(dataframe)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Шлях до файлу бази даних
    db_file = 'path/to/database.db'

    # Створення головного вікна
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
