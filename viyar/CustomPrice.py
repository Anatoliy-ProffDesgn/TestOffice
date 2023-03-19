import json
import os

from PyQt5.QtWidgets import QMessageBox


# data = [...]  # дані для порівняння
def get_first_column_as_list(tree_viwer):
    values = []
    model = tree_viwer.model()
    for row in range(model.rowCount()):
        index = model.index(row, 0)
        values.append(index.data())
    return values


def create_and_save(data, tree_viwer, rewrite=False):
    # Ім'я файлу для зберігання цін користувача
    if tree_viwer.model().rowCount() > 0:
        filename = "Custom/customPrice.json"

        # Завантаження даних з файлу customPrice.json, якщо він існує
        try:
            with open(filename, "r") as f:
                custom_prices = json.load(f)
        except FileNotFoundError:
            custom_prices = []
        if rewrite:
            custom_prices = []

        # Беремо артикул зі списку обраних знаходимо відповідний рядок в data
        custom_list_art = get_first_column_as_list(tree_viwer)  # отримуєм артикули
        custom_data = []
        for custom_art in custom_list_art:
            for item in data:
                art = item['Article']
                if custom_art == art:
                    custom_data.append(item)
                    break

        # Перевіряємо наявність рядків у збереженому файлі "Custom/customPrice.json"
        for item in custom_data:
            article = item["Article"]
            already_in_list = False
            # Перевіряємо, чи елемент вже є в списку
            for custom_item in custom_prices:
                if article == custom_item["Article"]:
                    already_in_list = True
                    break
            # Якщо елемента немає в списку, то додаємо його
            if not already_in_list:
                custom_prices.append(item)

        # Зберігаємо оновлений список в customPrise.json
        with open(filename, "w") as f:
            json.dump(custom_prices, f)
            return True


def save_custom_price(data, tree_view, rewrite=False):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle("Збереження файлу")
    # Ваш код для збереження файлу
    if create_and_save(data, tree_view, rewrite):
        # Показ повідомлення про збереження файлу
        msg_box.setText("Файл збережено")
    else:
        msg_box.setText("Щось пішло не за планом.\n" + 'Не владолось зберегти файл.')
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

    # Дерево порожнє