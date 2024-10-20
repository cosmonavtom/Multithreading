import socket
import threading

HOST = "127.0.0.1"
PORT = 50131


def handle_connection(sock, addr):
    shutdown = False  # Запустил ли клиент выключение сервера

    with sock:
        print("Подключение по", addr)
        while True:
            # Recieve
            try:
                data = sock.recv(1024)
                # Если данные пустые, значит клиент отключился. Убираем зацикливание при выходе клиента
                if not data:
                    print(f"Клиент отключился")
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
                print(f"Клиент внезапно отключился не могу отправить данные")
                break
        print("Отключение по", addr)




if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen(1)
        while True:
            shutdown = False  # Запустил ли клиент выключение сервера
            print("Ожидаю подключения....")
            sock, addr = serv_sock.accept()
            thread = threading.Thread(target=handle_connection, args=(sock, addr))
            print(thread)
            thread.start()
            if shutdown:
                break
