import socket

HOST = "127.0.0.1"
PORT = 50432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:

        # Проверка на отправку пустого сообщения
        while True:
            data = input("Напечатайте сообщение для отправки. Exit - отключение от сервера.\nShutdown - отключение сервера. Введите запрос: ")
            if data != '':
                break

        if data.strip().lower() in ['exit', 'quit']:
            print("Вы отключились от сервера")
            break

        try:
            data_bytes = data.encode()
            sock.sendall(data_bytes)
            data_bytes = sock.recv(1024)
            data = data_bytes.decode()
            print("Received:", data)
        except ConnectionAbortedError as ex:
            print(ex)
            break

print("Подключение разорвано...")
