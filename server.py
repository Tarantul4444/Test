import socket
import threading
# import sqlite3
#
# con = sqlite3.connect("clients.db")
# cur = con.cursor()

host = '127.0.0.1'
port = 7976

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} ушел!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print('Соединён с {}'.format(str(address)))
        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print('Имя пользователя {}'.format(nickname))
        broadcast('{} присоединился!'.format(nickname).encode('utf-8'))
        client.send('Подключён к серверу!'.encode('utf-8'))
        # for row in cur.execute('SELECT message FROM client'):
        #     client.send(row)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
