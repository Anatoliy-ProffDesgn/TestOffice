import datetime
import sqlite3
from threading import Lock
lock = Lock()
# import Parse_menu_viyar as p_menu
def correct_simbol(me_str, simbol='_'):
    cor = ['\'', '"', ';', ':', ',', '|', '(', ')', '[', ']', '{', '}', '<', '>', '=', '+', '-', '*', '/', '\\', '%', '&', '^', '$', '#', '@', '!', '?', '~', '`']
    for i in cor:
        if i in me_str:
            me_str = me_str.replace(i, simbol)
            print(me_str)
    return me_str

def get_table_list(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    conn.text_factory = lambda x: str(x, 'utf-8')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_list = [t[0] for t in cursor.fetchall()]
    conn.close()
    return table_list


def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    # print(f"Таблиця з таким назвою вже існує: {table_name}")
    return bool(cursor.fetchone())


def delete_table(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"Видалено таблицю: {table_name}")


def new_table(db_name, table_name, columns, del_old_table=True):
    # підключення до бази даних
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    conn.text_factory = lambda x: str(x, 'utf-8')
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


def insert_into_table(db_name, table_name, data):
    # підключення до бази даних
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    conn.text_factory = lambda x: str(x, 'utf-8')
    # table_name = 'my_table'
    with conn:
        # cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (article INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL, quality TEXT, category TEXT, subcategory TEXT, subsubcategory TEXT, image BLOB, data TEXT)")

        # формуємо список з кортежами для вставки у таблицю
        values = [(v['article'], v['name'], v['price'], v['quality'], v['category'], v['subcategory'],
                   v['subsubcategory'], v['image'], v['data']) for v in [data]]

        # Виконуємо запит на вставку даних з використанням executemany для додавання кількох рядків у таблицю
        cur.executemany(
            f"INSERT INTO {table_name} (article, name, price, quality, category, subcategory, subsubcategory, image, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            values)

    # Зберігаємо зміни та закриваємо з'єднання з базою даних
    conn.commit()
    conn.close()


def create_table_text(db_name, table_name, dicts, del_old_table=True):
    if type(dicts) != list:
        dicts = [dicts]
    # підключення до бази даних
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    conn.text_factory = lambda x: str(x, 'utf-8')
    # якщо таблиця з таким іменем існує, то видаляємо її
    if table_exists(cur, table_name):
        if del_old_table:
            delete_table(cur, table_name)

    conn.text_factory = lambda x: str(x, 'utf-8')
    with conn:
        # отримуємо список стовпців зі словника
        columns = list(dicts[0].keys())
        # створення таблиці
        cur.execute(
            "CREATE TABLE IF NOT EXISTS " + table_name + " (" + ", ".join([f"{col} TEXT" for col in columns]) + ")")
        # вставка даних
        for values in dicts:
            # формуємо рядок для вставки даних
            # Формування переліку стовпців таблиці
            column_list = []
            for col in columns:
                column_list.append(f'{col}')
            column_list_str = ", ".join(column_list)

            # Формування переліку значень для додавання у таблицю
            value_list = []
            for col in columns:
                me_str = values[col]
                if "'" in me_str:
                    me_str = me_str.replace("'", "''")
                value_list.append(f"'{me_str}'")
            value_list_str = ", ".join(value_list)

            # Складання запиту на додавання запису у таблицю з використанням змінних
            insert_sql = f"INSERT INTO {table_name} ({column_list_str}) VALUES ({value_list_str})"
            cur.execute(insert_sql)
    conn.commit()
    conn.close()
    print(f"Внесено зміни/створено таблицю: {table_name} у базі даних {db_name}")


def add_column_if_not_exists(db_name, table_name, column_name, data_type):
    # підключення до бази даних
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    conn.text_factory = lambda x: str(x, 'utf-8')
    with conn:
        # перевірка наявності стовпця
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = cur.fetchall()
        column_exists = False
        for col in columns:
            if col[1] == column_name:
                column_exists = True
                break
        # додавання стовпця, якщо він не існує
        if not column_exists:
            cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type}")
            print(f"Стовпець {column_name} додано до таблиці {table_name} у базі даних {db_name}")
        else:
            print(f"Стовпець {column_name} вже існує у таблиці {table_name} у базі даних {db_name}")
        conn.commit()
    conn.close()


def update_table(db_name, table_name, column_to_update, new_value, id):
    # підключення до бази даних
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    conn.text_factory = lambda x: str(x, 'utf-8')
    with conn:
        # оновлення значення в таблиці
        old_value = cur.execute(f"SELECT {column_to_update} FROM {table_name} WHERE rowid={id}").fetchone()[0]
        cur.execute(f"UPDATE {table_name} SET {column_to_update} = ? WHERE rowid = ?", (new_value, id))
        conn.commit()
    conn.close()
    print(f"Зміна значення: {db_name}/{table_name}|{column_to_update}| '{old_value}' змінено на '{new_value}'")


def select_from_table(db_name, table_name):
    # підключення до бази даних
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    conn.text_factory = lambda x: str(x, 'utf-8')
    # cur.execute(f"SELECT * FROM {table_name}")  # вибірка всіх записів з таблиці
    cur.execute(f"SELECT rowid, * FROM {table_name}")  # вивести усі рядки данних і їх id
    # виведення результату запиту
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()


if __name__ == '__main__':
    me_data = datetime.datetime.today().strftime('%d_%m_%Y')
    db_name = 'DataBase.db'
    tabl_name = f"log_update_{me_data}"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    data = {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Cleaf',
             'link': 'https://viyar.ua/excel_export/?id=2483&to_xls=Y&lang=ua'}
    # delete_table(cur, tabl_name)
    # create_table_text("DataBase.db", f"log_update_{me_data}", data)
    # print(get_table_list(db_name))
    # add_column_if_not_exists(db_name, tabl_name, 'file_name', 'TEXT')
    # select_from_table(db_name, tabl_name)
    # update_table(db_name, tabl_name, 'file_name', str(datetime.datetime.now().time()), 4)
    select_from_table(db_name, tabl_name)
    # print(cur.execute('PRAGMA table_info(table_name)'))
