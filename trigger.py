import time
import socket
import keyboard
import threading
from random import randint


##############  SERVER ###################


clients = []
stop_threads = False


def server_main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7777))
        server.listen()
    except Exception as e:
        return print('\nNão foi possível iniciar o servidor!\n' + str(e))

    while True:
        global stop_threads
        if stop_threads:
            break
        client, addr = server.accept()
        clients.append(client)
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            print('You Pressed A Key!')
            break  # finishing the loop
        thread = threading.Thread(target=messages_treatment, args=[client])
        thread.start()


def messages_treatment(client):
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            msg = client.recv(2048)
            broadcast(msg, client)
        except Exception as e:
            delete_client(client)
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except Exception as e:
                delete_client(clientItem)


##############  CLIENT ###################


def delete_client(client):
    clients.remove(client)


def client_main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nNao foi possível se conectar ao servidor\n')
    # username = input('Usuário: ')
    time.sleep(3)
    username = str(randint(0, 9))
    print('\nConectado!')

    thread1 = threading.Thread(target=receive_messages, args=[client])
    thread2 = threading.Thread(target=send_messages, args=[client, username])

    thread1.start()
    thread2.start()


def receive_messages(client):
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg + '\n')
        except:
            print('\nNão foi possível permanacer conctado no servidor!\n')
            print('Precione <ENTER> para continuar...')
            client.close()
            break


def send_messages(client, username):
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except Exception as e:
            return


##############  ALL ###################


def close():
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            if keyboard.is_pressed('esc'):  # if key 'esc' is pressed
                print('You Pressed A Key!')
                stop_threads = True
        except:
            print('Another key')


thread_server = threading.Thread(target=server_main)
thread_client = threading.Thread(target=client_main)

thread_all = threading.Thread(target=close)

thread_all.start()
time.sleep(2)
thread_server.start()
time.sleep(2)
thread_client.start()
thread_server.join()
print('Finished')
