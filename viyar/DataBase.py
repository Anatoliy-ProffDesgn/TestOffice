# -*- coding: utf-8 -*-
import datetime
import sqlite3
from threading import Lock


# import Parse_menu_viyar as p_menu


class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.text_factory = lambda x: str(x, 'utf-8')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.lock = Lock()

    def correct_simbol(self, me_str, simbol='_', bad_simbol=''):
        cor = ['\'', '"', ';', ':', ',', '|', '(', ')', '[', ']', '{', '}', '<', '>', '=', '+', '-', '*', '/', '\\',
               '%', '&', '^', '$', '#', '@', '!', '?', '~', '`']
        if not bad_simbol == '':
            cor = bad_simbol
            if type(cor) == str:
                s = cor
                cor = []
                for i in s:
                    cor.append(i)

        for i in cor:
            if i in me_str:
                me_str = me_str.replace(i, simbol)
                print(me_str)
        return me_str

    def table_exists(self, table_name):
        self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        # print(f"Таблиця з таким назвою вже існує: {table_name}")
        return bool(self.cur.fetchone())

    def get_table_list(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_list = [t[0] for t in self.cur.fetchall()]
        print(f"_________Список таблиць: {table_list}")
        return table_list

    def get_table_columns(self, table_name):
        self.cur.execute(f"PRAGMA table_info('{table_name}')")
        columns = [col[1] for col in self.cur.fetchall()]
        print(f"_________Список колонок в таблиці: {columns}")
        return columns

    def get_rows_count(self, table_name):
        self.cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = self.cur.fetchone()[0]
        print(f"_________Кількість записів в таблиці: {count}")
        return count

    def delete_table(self, table_name):
        self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Видалено таблицю: {table_name}")

    def new_table(self, table_name, columns, del_old_table=True):
        # якщо таблиця з таким іменем існує, то видаляємо її
        if self.table_exists(table_name):
            if del_old_table:
                self.delete_table(table_name)
            else:
                return False
        # створення таблиці
        self.cur.execute("""CREATE TABLE {} ({});""".format(table_name, columns))
        self.conn.commit()  # зберігаємо зміни
        print(f"Створено таблицю: {table_name} у базі даних {self.db_name}")
        return True

    def create_table_price(self, table_name):
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                article INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                quality TEXT,
                category TEXT,
                subcategory TEXT,
                subsubcategory TEXT,
                image BLOB,
                data TEXT
            )
        """)
        print(f"Створено таблицю: {self.db_name} | {table_name}")
        self.get_table_columns(table_name)

    def insert_into_price(self, table_name, data):
        with self.lock:
            if not self.table_exists(table_name):
                self.create_table_price(table_name)
            values = [(v['article'], v['name'], v['price'], v['quality'], v['category'], v['subcategory'],
                       v['subsubcategory'], v['image'], v['data']) for v in [data]]

            self.cur.executemany(
                f"REPLACE INTO {table_name} (article, name, price, quality, category, subcategory, subsubcategory, image, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                values)
            self.conn.commit()  # Зберігаємо зміни та закриваємо з'єднання з базою даних

    def create_table_text(self, table_name, dicts, del_old_table=True):
        if type(dicts) != list:
            dicts = [dicts]
        self.conn.text_factory = lambda x: str(x, 'utf-8')
        # якщо таблиця з таким іменем існує, то видаляємо її
        if self.table_exists(table_name):
            if del_old_table:
                self.delete_table(table_name)

        self.conn.text_factory = lambda x: str(x, 'utf-8')
        with self.lock:
            # отримуємо список стовпців зі словника
            columns = list(dicts[0].keys())
            # створення таблиці
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS " + table_name + " (" + ", ".join([f"{col} TEXT" for col in columns]) + ")")
            # вставка даних
            for values in dicts:  # формуємо рядок для вставки даних
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
                self.cur.execute(insert_sql)
            self.conn.commit()
            print(f"Внесено зміни/створено {self.db_name}|{table_name}| <- {dicts}")

    def add_column_if_not_exists(self, table_name, column_name, data_type):
        with self.lock:
            # перевірка наявності стовпця
            self.cur.execute(f"PRAGMA table_info({table_name})")
            columns = self.cur.fetchall()
            column_exists = False
            for col in columns:
                if col[1] == column_name:
                    column_exists = True
                    break
            # додавання стовпця, якщо він не існує
            if not column_exists:
                self.cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type}")
                print(f"Стовпець {column_name} додано до таблиці {table_name} у базі даних {self.db_name}")
            else:
                print(f"Стовпець {column_name} вже існує у таблиці {table_name} у базі даних {self.db_name}")
            self.conn.commit()

    def update_table(self, table_name, column_to_update, new_value, id):
        with self.lock:
            # оновлення значення в таблиці
            old_value = self.cur.execute(f"SELECT {column_to_update} FROM {table_name} WHERE rowid={id}").fetchone()[0]
            self.cur.execute(f"UPDATE {table_name} SET {column_to_update} = ? WHERE rowid = ?", (new_value, id))
            self.conn.commit()
            print(
                f"Зміна значення: {self.db_name}/{table_name}|{column_to_update}| '{old_value}' змінено на '{new_value}'")

    def find_duplicates(self, table_name, column_name):
        self.cur.execute(
            f"SELECT {column_name}, COUNT({column_name}) as count FROM {table_name} GROUP BY {column_name} HAVING COUNT({column_name}) > 1")
        # виведення результату запиту
        rows = self.cur.fetchall()
        return rows

    def select_find_in_column(self, table_name, column_name, search_value):
        # self.cur.execute(f"SELECT * FROM {table_name} WHERE {column_name}=?", (search_value,))
        self.cur.execute(f"SELECT * FROM {table_name} WHERE LOWER({column_name}) LIKE LOWER(?)", ('%' + search_value.lower() + '%',))
        rows = self.cur.fetchall()
        return rows

    def select_from_table(self, table_name):
        # self.cur.execute(f"SELECT * FROM {table_name}")  # вибірка всіх записів з таблиці
        self.cur.execute(f"SELECT rowid, * FROM {table_name}")  # вивести усі рядки данних і їх id
        # виведення результату запиту
        rows = self.cur.fetchall()
        return rows

    def select_from_table_sorted(self, table_name, column_name, reverse=False):
        direction = "DESC" if reverse else "ASC"
        self.cur.execute(f"SELECT rowid as id, * FROM {table_name} ORDER BY {column_name} {direction}")
        # виведення результату запиту
        rows = self.cur.fetchall()
        return rows

    def select_from_table_double_sorted(self, table_name, column_name_1, column_name_2, reverse=False):
        direction = "DESC" if reverse else "ASC"
        self.cur.execute(
            f"SELECT rowid as id, * FROM {table_name} ORDER BY {column_name_1}, {column_name_2} {direction}")
        # виведення результату запиту
        rows = self.cur.fetchall()
        return rows

    def select_row_by_id(self, table_name, id):
        self.cur.execute(f"SELECT * FROM {table_name} WHERE rowid=?", (id,))
        row = self.cur.fetchone()
        # if row is None:
        #     return [f"Рядок з id={id} не знайдено в таблиці {table_name}"]
        return row

    def select_unique_values(self, table_name, column_name):
        self.cur.execute(f"SELECT DISTINCT {column_name} FROM {table_name}")
        # виведення результату запиту
        rows = self.cur.fetchall()
        return rows

    def close(self):
        self.conn.close()


def info_table(tabl_name):  # _________info_________
    print('\n_________info_________')
    try:
        db.get_table_list()
    except:
        pass
    print(f'_________Спробуємо отримати таблицю: {tabl_name}')
    try:
        db.get_table_columns(tabl_name)
    except:
        print(f'_________Таблиця не знайдена {tabl_name}\n')
        pass
    try:
        db.get_rows_count(tabl_name)
    except:
        print(f'_________Таблиця не знайдена {tabl_name}\n')
        pass
    print('\n')


if __name__ == '__main__':
    i = 0
    me_data = datetime.datetime.today().strftime('%d_%m_%Y')
    db = DataBase('DataBase.db')
    tabs = db.get_table_list()
    num = None
    for t in tabs:
        i += 1
        print(f"{i}) {t}")
    while num is None:
        try:
            num = int(input("Оберіть номер таблиці: №: ")) - 1
        except:
            pass
    info_table(tabs[num])
    # _______test_________
    # db.delete_table(tabs[num])
    # db.create_table_text(f"log_update_{me_data}", data)
    # db.add_column_if_not_exists(tabs[num], 'file_name', 'TEXT')
    # db.update_table(tabl_name, 'tabs[num]', str(datetime.datetime.now().time()), 4)
    # rows = db.select_from_table(tabs[num])
    # rows = db.select_from_table_sorted(tabs[num], 'article')
    # rows = db.select_from_table_double_sorted(tabs[num], 'cat', 'rozdil')
    # rows = db.select_row_by_id(tabs[num], 20)
    # rows = db.find_duplicates(tabs[num], 'article')
    # rows = db.select_unique_values(tabs[num], 'subcategory')
    rows = db.select_find_in_column(tabs[num], 'subcategory', 'Побутова')

    if len(rows) == 0:
        print(f'_________Не знайдено в {tabs[num]}\n')
    else:
        for row in rows:
            i += 1
            # if i/4000 in [0.1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]:
            #     input(f'\n{i} Enter to continue\n')
            print(list(row))
        print(len(rows))
        info_table(tabs[num])
