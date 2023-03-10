import socket


def is_internet_available():
    try:
        # Спроба створення з'єднання з віддаленим сервером за допомогою HTTP-запиту
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


if __name__ == "__main__":
    print(is_internet_available())
