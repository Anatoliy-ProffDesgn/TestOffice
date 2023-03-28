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

    def get_table_list(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_list = [t[0] for t in self.cur.fetchall()]
        print(f"_________Список таблиць: {table_list}")
        return table_list

    def table_exists(self, table_name):
        self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        # print(f"Таблиця з таким назвою вже існує: {table_name}")
        return bool(self.cur.fetchone())

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
                article TEXT PRIMARY KEY,
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

    def select_from_table(self, table_name):
        # self.cur.execute(f"SELECT * FROM {table_name}")  # вибірка всіх записів з таблиці
        self.cur.execute(f"SELECT rowid, * FROM {table_name}")  # вивести усі рядки данних і їх id
        # виведення результату запиту
        rows = self.cur.fetchall()
        results = []
        for row in rows:
            results.append(list(row))
            print(list(row))
        return rows

    def select_from_table_sorted(self, table_name, column_name, reverse=False):
        self.conn.text_factory = lambda x: str(x, 'utf-8')
        direction = "DESC" if reverse else "ASC"
        self.cur.execute(f"SELECT * FROM {table_name} ORDER BY {column_name} {direction}")
        # виведення результату запиту
        rows = self.cur.fetchall()
        results = []
        for row in rows:
            results.append(list(row))
            print(list(row))
        # return results
        return rows

    def select_from_table_double_sorted(self, table_name, column_name_1, column_name_2, reverse=False):
        self.conn.text_factory = lambda x: str(x, 'utf-8')
        direction = "DESC" if reverse else "ASC"
        self.cur.execute(f"SELECT * FROM {table_name} ORDER BY {column_name_1}, {column_name_2} {direction}")
        # виведення результату запиту
        rows = self.cur.fetchall()
        results = []
        for row in rows:
            results.append(list(row))
            print(list(row))
        # return results
        return rows

    def select_row_by_id(self, table_name, id):
        self.cur.execute(f"SELECT * FROM {table_name} WHERE rowid=?", (id,))
        row = self.cur.fetchone()
        if row is not None:
            # Друкуємо знайдений рядок на екран
            print(list(row))
        else:
            print(f"Рядок з id={id} не знайдено в таблиці {table_name}")
        return row

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
    data = [{'cat': 'Плитні матеріали', 'rozdil': 'ХДФ / ДВП | ДВП Уніплит',
             'link': 'https://viyar.ua/excel_export/?id=3239&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Swiss Krono',
             'link': 'https://viyar.ua/excel_export/?id=2492&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | AGT',
             'link': 'https://viyar.ua/excel_export/?id=2510&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | Kronospan',
             'link': 'https://viyar.ua/excel_export/?id=2512&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Навіси меблеві',
             'link': 'https://viyar.ua/excel_export/?id=2540&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки для отворів під ручку',
             'link': 'https://viyar.ua/excel_export/?id=3287&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | Панелі МДФ Cleaf Piombo',
             'link': 'https://viyar.ua/excel_export/?id=3161&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Різні метизи',
             'link': 'https://viyar.ua/excel_export/?id=2529&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Тримачі дзеркал',
             'link': 'https://viyar.ua/excel_export/?id=3309&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки для завіс',
             'link': 'https://viyar.ua/excel_export/?id=3288&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Завіси й аксесуари | Аксесуари',
             'link': 'https://viyar.ua/excel_export/?id=2567&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Дюбелі',
             'link': 'https://viyar.ua/excel_export/?id=2524&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Герметики, силікони',
             'link': 'https://viyar.ua/excel_export/?id=3073&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Ніжки, ролики, опори | Ніжки',
             'link': 'https://viyar.ua/excel_export/?id=2546&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | МДФ (інші)',
             'link': 'https://viyar.ua/excel_export/?id=2988&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Консолі',
             'link': 'https://viyar.ua/excel_export/?id=3311&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки для саморізів',
             'link': 'https://viyar.ua/excel_export/?id=3290&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Ніжки, ролики, опори | Опори',
             'link': 'https://viyar.ua/excel_export/?id=2548&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Комплектуючі для ліжок | Каркаси для ліжок',
             'link': 'https://viyar.ua/excel_export/?id=2982&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Завіси й аксесуари | Завіси',
             'link': 'https://viyar.ua/excel_export/?id=2566&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': "Панелі для інтер'єру | Панелі HAUTE MATERIAL",
             'link': 'https://viyar.ua/excel_export/?id=2518&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Ручки та гачки | Ручки-профіль',
             'link': 'https://viyar.ua/excel_export/?id=2544&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Борти кухонні і цоколі | Цоколі та комплектуючі',
             'link': 'https://viyar.ua/excel_export/?id=2570&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Релінги і комплектуючі | Релінги та кріплення',
             'link': 'https://viyar.ua/excel_export/?id=2564&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Пакувальний матеріал | Стретч',
             'link': 'https://viyar.ua/excel_export/?id=3209&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Комплектуючі для ліжок | Підйомні механізми для ліжок',
             'link': 'https://viyar.ua/excel_export/?id=2983&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Клей HENKEL',
             'link': 'https://viyar.ua/excel_export/?id=2583&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Вентиляційні решітки',
             'link': 'https://viyar.ua/excel_export/?id=3286&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | DDL',
             'link': 'https://viyar.ua/excel_export/?id=3079&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Конфірмати',
             'link': 'https://viyar.ua/excel_export/?id=2525&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Комплектуючі для модульної системи | Scilm',
             'link': 'https://viyar.ua/excel_export/?id=3148&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Шухляди MullerBox',
             'link': 'https://viyar.ua/excel_export/?id=2535&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Ручки та гачки | Профілі Gola',
             'link': 'https://viyar.ua/excel_export/?id=3277&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | Kastamonu',
             'link': 'https://viyar.ua/excel_export/?id=3131&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Тримачі для полиць',
             'link': 'https://viyar.ua/excel_export/?id=3308&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Клей двокомпонентний',
             'link': 'https://viyar.ua/excel_export/?id=3074&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки для дротів',
             'link': 'https://viyar.ua/excel_export/?id=3289&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Метабокси',
             'link': 'https://viyar.ua/excel_export/?id=2532&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Сушки і піддони',
             'link': 'https://viyar.ua/excel_export/?id=2542&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Ніжки, ролики, опори | Ролики',
             'link': 'https://viyar.ua/excel_export/?id=2547&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки самоклеючі',
             'link': 'https://viyar.ua/excel_export/?id=3292&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'ХДФ / ДВП | ХДФ Pfleiderer',
             'link': 'https://viyar.ua/excel_export/?id=2508&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'Пластик HPL | Fenix',
             'link': 'https://viyar.ua/excel_export/?id=2919&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Шухляди ArciTech',
             'link': 'https://viyar.ua/excel_export/?id=2533&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | Kronospan',
             'link': 'https://viyar.ua/excel_export/?id=2607&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Кошики, відра, магічні кути',
             'link': 'https://viyar.ua/excel_export/?id=2539&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Кабінетні куточки',
             'link': 'https://viyar.ua/excel_export/?id=3310&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Пакувальний матеріал | Скотч',
             'link': 'https://viyar.ua/excel_export/?id=3210&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': "Панелі для інтер'єру | Стінові панелі AGT",
             'link': 'https://viyar.ua/excel_export/?id=2937&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Направляючі',
             'link': 'https://viyar.ua/excel_export/?id=2531&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Релінги і комплектуючі | Полиці для релінгу',
             'link': 'https://viyar.ua/excel_export/?id=2563&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Колони',
             'link': 'https://viyar.ua/excel_export/?id=2728&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Саморізи',
             'link': 'https://viyar.ua/excel_export/?id=2528&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Заглушки меблеві | Заглушки пластикові',
             'link': 'https://viyar.ua/excel_export/?id=3291&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Накладки для стільниць',
             'link': 'https://viyar.ua/excel_export/?id=2541&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | Niemann',
             'link': 'https://viyar.ua/excel_export/?id=2495&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'ХДФ / ДВП | ХДФ Kronospan',
             'link': 'https://viyar.ua/excel_export/?id=2507&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Ніжки, ролики, опори | Допоміжна фурнітура',
             'link': 'https://viyar.ua/excel_export/?id=2549&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'Пластик HPL | Arpa',
             'link': 'https://viyar.ua/excel_export/?id=2920&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'Фанера | Фанера вологостійка',
             'link': 'https://viyar.ua/excel_export/?id=2520&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'OSB | OSB/3 Swiss Krono',
             'link': 'https://viyar.ua/excel_export/?id=2516&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | Egger',
             'link': 'https://viyar.ua/excel_export/?id=2511&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Комплектуючі для модульної системи | Cosma',
             'link': 'https://viyar.ua/excel_export/?id=3149&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Ручки та гачки | Гачки меблеві',
             'link': 'https://viyar.ua/excel_export/?id=2560&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Організації для висувних шухляд',
             'link': 'https://viyar.ua/excel_export/?id=3049&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Шухляди Atira',
             'link': 'https://viyar.ua/excel_export/?id=2536&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Полицетримачі | Монтажні куточки',
             'link': 'https://viyar.ua/excel_export/?id=3312&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Egger',
             'link': 'https://viyar.ua/excel_export/?id=2484&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Висувні механізми | Шухляди AvanTech YOU',
             'link': 'https://viyar.ua/excel_export/?id=2990&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Кухонні комплектуючі | Карго',
             'link': 'https://viyar.ua/excel_export/?id=2538&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Стяжки',
             'link': 'https://viyar.ua/excel_export/?id=2527&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Клей для стільниць',
             'link': 'https://viyar.ua/excel_export/?id=2584&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Kronospan',
             'link': 'https://viyar.ua/excel_export/?id=2490&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | Лаковані панелі МДФ',
             'link': 'https://viyar.ua/excel_export/?id=2806&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'МДФ-плита | Коростень',
             'link': 'https://viyar.ua/excel_export/?id=2513&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Гвинти',
             'link': 'https://viyar.ua/excel_export/?id=2523&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Saviola',
             'link': 'https://viyar.ua/excel_export/?id=2493&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Метизна продукція | Муфти',
             'link': 'https://viyar.ua/excel_export/?id=2526&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стінові панелі | Kronospan',
             'link': 'https://viyar.ua/excel_export/?id=2615&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'Фасадні МДФ-панелі | Панелі МДФ RAUVISIO Crystal',
             'link': 'https://viyar.ua/excel_export/?id=2499&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | RICCI',
             'link': 'https://viyar.ua/excel_export/?id=2773&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Борти кухонні і цоколі | Бортики кухонні і комплектуючі',
             'link': 'https://viyar.ua/excel_export/?id=2569&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Ручки та гачки | Ручки меблеві',
             'link': 'https://viyar.ua/excel_export/?id=2561&to_xls=Y&lang=ua'},
            {'cat': 'Меблева фурнітура', 'rozdil': 'Промислова хімія | Клей монтажний',
             'link': 'https://viyar.ua/excel_export/?id=3075&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Компакт-плита | Egger',
             'link': 'https://viyar.ua/excel_export/?id=3186&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Компакт-плита | Fenix',
             'link': 'https://viyar.ua/excel_export/?id=3184&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | RICCI',
             'link': 'https://viyar.ua/excel_export/?id=2949&to_xls=Y&lang=ua'},
            {'cat': 'Плитні матеріали', 'rozdil': 'ДСП | Cleaf',
             'link': 'https://viyar.ua/excel_export/?id=2483&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | Arpa',
             'link': 'https://viyar.ua/excel_export/?id=2609&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Kromag',
             'link': 'https://viyar.ua/excel_export/?id=2591&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стінові панелі | LuxeForm',
             'link': 'https://viyar.ua/excel_export/?id=2614&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | Egger',
             'link': 'https://viyar.ua/excel_export/?id=2611&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Egger',
             'link': 'https://viyar.ua/excel_export/?id=2883&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | LuxeForm',
             'link': 'https://viyar.ua/excel_export/?id=2608&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стінові панелі | Egger',
             'link': 'https://viyar.ua/excel_export/?id=2613&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Rehau',
             'link': 'https://viyar.ua/excel_export/?id=2588&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Компакт-плита | Arpa',
             'link': 'https://viyar.ua/excel_export/?id=3180&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Амбарний механізм',
             'link': 'https://viyar.ua/excel_export/?id=2780&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Swiss Krono',
             'link': 'https://viyar.ua/excel_export/?id=2601&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Компакт-плита | Fundermax',
             'link': 'https://viyar.ua/excel_export/?id=3185&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Arpa',
             'link': 'https://viyar.ua/excel_export/?id=2599&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стінові панелі | Arpa',
             'link': 'https://viyar.ua/excel_export/?id=2929&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Kronospan',
             'link': 'https://viyar.ua/excel_export/?id=2602&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Пластик | Luxeform',
             'link': 'https://viyar.ua/excel_export/?id=2600&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Niemann',
             'link': 'https://viyar.ua/excel_export/?id=2593&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Шпонована',
             'link': 'https://viyar.ua/excel_export/?id=2905&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Направляючий профіль',
             'link': 'https://viyar.ua/excel_export/?id=2873&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Rehau лазерна',
             'link': 'https://viyar.ua/excel_export/?id=2595&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Maag',
             'link': 'https://viyar.ua/excel_export/?id=3169&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Hranipex',
             'link': 'https://viyar.ua/excel_export/?id=2592&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Polkemic',
             'link': 'https://viyar.ua/excel_export/?id=2943&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Вертикальний профіль',
             'link': 'https://viyar.ua/excel_export/?id=2627&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Меламінова з клеєм',
             'link': 'https://viyar.ua/excel_export/?id=2597&to_xls=Y&lang=ua'},
            {'cat': 'Стільниці та стінпанелі', 'rozdil': 'Стільниці (на основі ДСП) | Swiss Krono',
             'link': 'https://viyar.ua/excel_export/?id=2610&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи',
                                                                                  'rozdil': 'Розсувні системи Starke | Фурнітура для розсувної системи',
                                                                                  'link': 'https://viyar.ua/excel_export/?id=2643&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Egger',
             'link': 'https://viyar.ua/excel_export/?id=2589&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Складна система Starke-W',
             'link': 'https://viyar.ua/excel_export/?id=2896&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Профіль Connect',
             'link': 'https://viyar.ua/excel_export/?id=2644&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи',
                                                                                  'rozdil': 'Розсувні системи Hettich | Розсувна система SlideLine 55',
                                                                                  'link': 'https://viyar.ua/excel_export/?id=2648&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Складна система WingLine 230',
             'link': 'https://viyar.ua/excel_export/?id=2653&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Складна система WingLine L',
             'link': 'https://viyar.ua/excel_export/?id=2772&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | AGT',
             'link': 'https://viyar.ua/excel_export/?id=2594&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи',
                                                                                  'rozdil': 'Розсувні системи Hettich | Розсувна система TopLine XL v2.0',
                                                                                  'link': 'https://viyar.ua/excel_export/?id=3047&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи',
             'rozdil': 'Розсувні системи Terno Scorrevoli | Розсувна система Dama',
             'link': 'https://viyar.ua/excel_export/?id=3121&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Профіль Compact',
             'link': 'https://viyar.ua/excel_export/?id=2925&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Аксесуари',
             'link': 'https://viyar.ua/excel_export/?id=2651&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Ario | Супутня фурнітура Ario',
             'link': 'https://viyar.ua/excel_export/?id=2658&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Розсувна система Glatt',
             'link': 'https://viyar.ua/excel_export/?id=2645&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Гардеробна система Eureka | Комплектуючі Eureka',
             'link': 'https://viyar.ua/excel_export/?id=2795&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Ario | Направляючий профіль Ario',
             'link': 'https://viyar.ua/excel_export/?id=2657&to_xls=Y&lang=ua'},
            {'cat': 'Крайки та пластики', 'rozdil': 'Крайка | Cleaf',
             'link': 'https://viyar.ua/excel_export/?id=2590&to_xls=Y&lang=ua'},
            {'cat': 'Меблі', 'rozdil': 'Готові дзеркала | Дзеркала без підсвічування',
             'link': 'https://viyar.ua/excel_export/?id=3243&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Ario | Горизонтальний профіль Ario',
             'link': 'https://viyar.ua/excel_export/?id=2656&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи',
                                                                                  'rozdil': 'Розсувні системи Hettich | Розсувна система TopLine L v2.0',
                                                                                  'link': 'https://viyar.ua/excel_export/?id=3046&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Кухонні комплектуючі | Фільтри для води Ecosoft',
             'link': 'https://viyar.ua/excel_export/?id=2821&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Ario | Вертикальний профіль Ario',
             'link': 'https://viyar.ua/excel_export/?id=2655&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи',
                                                                                  'rozdil': 'Міжкімнатні системи Terno Scorrevoli | Розсувна система Diva air Vetro',
                                                                                  'link': 'https://viyar.ua/excel_export/?id=3123&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Starke | Горизонтальний профіль',
             'link': 'https://viyar.ua/excel_export/?id=2634&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи',
                                                                                  'rozdil': 'Розсувні системи Terno Scorrevoli | Компланарна система Switch',
                                                                                  'link': 'https://viyar.ua/excel_export/?id=3117&to_xls=Y&lang=ua'},
            {'cat': 'Скло та дзеркало', 'rozdil': 'Скло та дзеркало',
             'link': 'https://viyar.ua/excel_export/?id=2514&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Розсувні системи Hettich | Розсувна система SlideLine M',
             'link': 'https://viyar.ua/excel_export/?id=2652&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Кавомашини',
             'link': 'https://viyar.ua/excel_export/?id=2998&to_xls=Y&lang=ua'}, {'cat': 'Дверні та гардеробні системи',
                                                                                  'rozdil': 'Міжкімнатні системи Terno Scorrevoli | Розсувна система Magic 2',
                                                                                  'link': 'https://viyar.ua/excel_export/?id=3119&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи',
             'rozdil': 'Міжкімнатні системи Terno Scorrevoli | Розсувна система Vetro 40',
             'link': 'https://viyar.ua/excel_export/?id=3125&to_xls=Y&lang=ua'},
            {'cat': 'Дверні та гардеробні системи', 'rozdil': 'Гардеробна система Eureka | Комплекти Eureka',
             'link': 'https://viyar.ua/excel_export/?id=3165&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Варильні поверхні',
             'link': 'https://viyar.ua/excel_export/?id=2955&to_xls=Y&lang=ua'},
            {'cat': 'Меблі', 'rozdil': 'Готові дзеркала | Дзеркала з підсвічуванням',
             'link': 'https://viyar.ua/excel_export/?id=3267&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Кухонні плити',
             'link': 'https://viyar.ua/excel_export/?id=3316&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Холодильна техніка',
             'link': 'https://viyar.ua/excel_export/?id=2968&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Мікрохвильові печі',
             'link': 'https://viyar.ua/excel_export/?id=2958&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Витяжки',
             'link': 'https://viyar.ua/excel_export/?id=2683&to_xls=Y&lang=ua'},
            {'cat': 'Вироби з каменю', 'rozdil': 'Кварцит | Caesarstone',
             'link': 'https://viyar.ua/excel_export/?id=3194&to_xls=Y&lang=ua'},
            {'cat': 'Вироби з каменю', 'rozdil': 'Широкоформатний керамограніт | Inalco',
             'link': 'https://viyar.ua/excel_export/?id=3196&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Кухонні комплектуючі | Вентиляційні системи',
             'link': 'https://viyar.ua/excel_export/?id=2798&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Кухонні комплектуючі | Мийки та аксесуари',
             'link': 'https://viyar.ua/excel_export/?id=2676&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Кухонні комплектуючі | Змішувачі',
             'link': 'https://viyar.ua/excel_export/?id=2691&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Пральні машини',
             'link': 'https://viyar.ua/excel_export/?id=2967&to_xls=Y&lang=ua'}, {'cat': 'Побутова техніка',
                                                                                  'rozdil': 'Велика побутова техніка | Фурнітура для встановлення вбудованої техніки',
                                                                                  'link': 'https://viyar.ua/excel_export/?id=3226&to_xls=Y&lang=ua'},
            {'cat': 'Вироби з каменю', 'rozdil': 'Штучний акриловий камінь | Grandex',
             'link': 'https://viyar.ua/excel_export/?id=3233&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Підкладки | ДВП',
             'link': 'https://viyar.ua/excel_export/?id=3100&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Посудомийні машини',
             'link': 'https://viyar.ua/excel_export/?id=2743&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Коркове покриття | Egger Comfort',
             'link': 'https://viyar.ua/excel_export/?id=3114&to_xls=Y&lang=ua'},
            {'cat': 'Вироби з металу', 'rozdil': 'Вироби з металу',
             'link': 'https://viyar.ua/excel_export/?id=3257&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Композитне покриття | Egger Design GreenTec',
             'link': 'https://viyar.ua/excel_export/?id=3111&to_xls=Y&lang=ua'},
            {'cat': 'Вироби з каменю', 'rozdil': 'Широкоформатний керамограніт | Neolith',
             'link': 'https://viyar.ua/excel_export/?id=3195&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Підкладки | Коркова',
             'link': 'https://viyar.ua/excel_export/?id=3099&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Плінтуси та комплектуючі | KAINDL',
             'link': 'https://viyar.ua/excel_export/?id=3096&to_xls=Y&lang=ua'},
            {'cat': 'Побутова техніка', 'rozdil': 'Велика побутова техніка | Духові шафи',
             'link': 'https://viyar.ua/excel_export/?id=2957&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Ламінат | CLASSEN',
             'link': 'https://viyar.ua/excel_export/?id=3154&to_xls=Y&lang=ua'},
            {'cat': 'Вироби з каменю', 'rozdil': 'Штучний акриловий камінь | Getacore',
             'link': 'https://viyar.ua/excel_export/?id=3263&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Ламінат | KRONOPOL',
             'link': 'https://viyar.ua/excel_export/?id=3155&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Плінтуси та комплектуючі | FN Neuhofer Holz',
             'link': 'https://viyar.ua/excel_export/?id=3095&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Ламінат | KAINDL',
             'link': 'https://viyar.ua/excel_export/?id=3091&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Ламінат | EGGER',
             'link': 'https://viyar.ua/excel_export/?id=3092&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Плінтуси та комплектуючі | Arbiton',
             'link': 'https://viyar.ua/excel_export/?id=3204&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Підкладки | Полістирольна',
             'link': 'https://viyar.ua/excel_export/?id=3098&to_xls=Y&lang=ua'},
            {'cat': 'Освітлення для меблів', 'rozdil': 'Освітлення для меблів',
             'link': 'https://viyar.ua/excel_export/?id=2550&to_xls=Y&lang=ua'},
            {'cat': 'Інструменти і витратні матеріали', 'rozdil': 'Інструменти і витратні матеріали',
             'link': 'https://viyar.ua/excel_export/?id=2574&to_xls=Y&lang=ua'},
            {'cat': 'Покриття підлоги', 'rozdil': 'Плінтуси та комплектуючі | Cezar',
             'link': 'https://viyar.ua/excel_export/?id=3094&to_xls=Y&lang=ua'},
            {'cat': 'Виробничі послуги', 'rozdil': 'Виробничі послуги',
             'link': 'https://viyar.ua/excel_export/?id=2694&to_xls=Y&lang=ua'}]
    me_data = datetime.datetime.today().strftime('%d_%m_%Y')
    db = DataBase('DataBase.db')
    # tabl_name = 'log_update_26_03_2023'
    tabl_name = 'price_26_03_2023'
    # tabl_name = f"log_update_{me_data}"
    info_table(tabl_name)
    # _______test_________
    # db.delete_table(tabl_name)
    # db.create_table_text(f"log_update_{me_data}", data)
    # db.add_column_if_not_exists(tabl_name, 'file_name', 'TEXT')
    # db.update_table(tabl_name, 'file_name', str(datetime.datetime.now().time()), 4)
    db.select_from_table(tabl_name)
    # db.select_from_table_double_sorted(tabl_name, 'cat', 'rozdil')
    # db.select_row_by_id(tabl_name, 20)
    info_table(tabl_name)




