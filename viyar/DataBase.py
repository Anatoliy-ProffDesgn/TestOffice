import datetime
import sqlite3
import Parse_menu_viyar as p_menu


def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    print(f"Таблиця з таким назвою вже існує: {table_name}")
    return bool(cursor.fetchone())


def delete_table(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"Видалено таблицю: {table_name}")


def new_table(db_name, table_name, columns, del_old_table=True):
    # підключення до бази даних
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # якщо таблиця з таким іменем існує, то видаляємо її
    if table_exists(cur, table_name):
        if del_old_table:
            delete_table(cur, table_name)
        else:
            return False

    # створення таблиці
    cur.execute("""CREATE TABLE {} ({});""".format(table_name, columns))
    conn.commit()
    conn.close()
    print(f"Створено таблицю: {table_name} у базі даних {db_name}")
    return True

if __name__ == '__main__':
    # lst = p_menu.me_parse_menu()
    me_data = datetime.datetime.today().strftime('%d_%m_%Y')
    new_table("DataBase.db", f"price2_{me_data}", '''article INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    name TEXT NOT NULL,
                                                    price REAL,
                                                    quality TEXT,
                                                    category TEXT,
                                                    subcategory TEXT,
                                                    subsubcategory TEXT,
                                                    image BLOB,
                                                    data TEXT''')