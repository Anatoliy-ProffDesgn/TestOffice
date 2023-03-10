import json
import os


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

        custom_list_art = get_first_column_as_list(tree_viwer)
        custom_data = []
        for item in data:
            art = item['Article']
            for custom_art in custom_list_art:
                if custom_art == art:
                    custom_data.append(item)
                    break

        # Проходимо циклом по всіх елементах data
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
