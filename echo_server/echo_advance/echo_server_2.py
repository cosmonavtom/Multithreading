import socket

HOST = "127.0.0.1"  # Использовать все адреса: виден и снаружи, и изнутри
PORT = 50432  # Port to listen on (non-privileged ports are > 1023)

# Проверяем, что скрипт был запущен на исполнение, а не импортирован
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen()
        # Принимает множественные соединения, но только 1 в текущий момент
        while True:
            print("Ожидаю подключения....")
            sock, addr = serv_sock.accept()
            shutdown = False  # Запустил ли клиент выключение сервера

            with sock:
                print("Подключение по", addr)
                while True:
                    # Recieve
                    try:
                        data = sock.recv(1024)
                        # Если данные пустые, значит клиент отключился. Убираем зацикливание при выходе клиента
                        if not data:
                            print("Клиент отключился")
                            break
                        # Декодирование байтов в строку и отключение сервера по "stop server" и "shutdown"
                        decoded_data = data.decode('utf-8')
                        if decoded_data.strip().lower() in ['stop server', 'shutdown']:
                            print("Клиент ввел команду для отключения сервера")
                            print("Сервер отключён")
                            shutdown = True
                            break

                    except ConnectionError:
                        print("Клиент внезапно отключился в процессе отправки данных на сервер")
                        break

                    print(f"Получено: {data}, from: {addr}")
                    data = data.upper()
                    # Send
                    print(f"Send: {data} to: {addr}")
                    try:
                        sock.sendall(data)
                    except ConnectionError:
                        print(f"Клиент внезапно отключился, не могу отправить данные")
                        break

                print("Отключение по", addr)

            if shutdown:
                break
