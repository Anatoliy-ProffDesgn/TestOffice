import sqlite3

db=sqlite3.connect('testBase.db')
sql=db.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT,
    cash BIGINT
)''') # Создание таблицы

db.commit() # Сохранение изменений
