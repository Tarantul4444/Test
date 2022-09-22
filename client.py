import socket
import threading
# import sqlite3
#
# con = sqlite3.connect("clients.db")
# cur = con.cursor()

port = int(input('Введите порт: '))
while port != 7976:
    port = int(input('Введите порт заново: '))
nickname = input('Введите имя пользователя: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 7976))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        # cur.execute('''
        #             INSERT INTO clients VALUES
        #                 {message}
        #         '''.format())
        # con.commit()
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
