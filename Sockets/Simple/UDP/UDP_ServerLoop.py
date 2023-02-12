import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 8888))
while True:
    try:    # при помилці відправляємо повідомлення про помилку
        result = sock.recv(1024) # очікуємо повідомлення від клієнта
        # закрити якщо "q" або "Q" або "quit" або "Quit"
        if result.decode('utf-8') in ['q', 'Q', 'quit', 'Quit']:     # перевірка на повідомлення про закриття
            print('Message:', 'Вихід')     # виводимо повідомлення
            sock.close()  # закриваємо сокет
            break     # виходимо з циклу
    except KeyboardInterrupt:                 # перевіряємо чи нам прийшло спеціальне повідомлення
        print('Message:', 'Exit')     # виводимо повідомлення
        sock.close()                    # закриваємо сокет
        break                         # виходимо з циклу
    else:                            # при відповіді клієнта виводимо його повідомлення
        print('Message', result.decode('utf-8'))    # виводимо повідомлення від клієнта