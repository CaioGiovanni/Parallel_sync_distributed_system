import time
import socket
import keyboard
import threading

from random import randint

chave = ['time1', 'time2', 'time3', 'time4']
time_ganhador = []
trigger_send_msg = False


##############  SERVER ###################


clients = []
servers = [('localhost', 7777), ('localhost', 5000)]
stop_threads = False
first_exec_connect = True


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
        thread = threading.Thread(target=messages_treatment, args=[client])
        thread.start()
        if trigger_send_msg:
            broadcast(str(time_ganhador).encode('utf-8'), client)


def messages_treatment(client):
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            msg = client.recv(2048)
            if 'Me mande a chave' in str(msg):
                update_chave(str(time_ganhador).encode('utf-8'), client)
            else:
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


def update_chave(msg, client):
    for clientItem in clients:
        if clientItem == client:
            try:
                clientItem.send(msg)
            except Exception as e:
                delete_client(clientItem)


def delete_client(client):
    clients.remove(client)


##############  CLIENT ###################


def client_main(ip, host):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', host))  # CONNECT TO FIRST EXEC
    except:
        return print('\nNao foi possível se conectar ao servidor\n')
    # username = input('Usuário: ')
    time.sleep(3)
    username = str(randint(0, 100))

    if first_exec_connect:
        request = 'Me mande a chave'
    else:
        request = None

    print(f'\n{username} - Conectado!')

    thread1 = threading.Thread(target=receive_messages, args=[client])
    thread2 = threading.Thread(target=send_messages, args=[client, username, request])

    thread1.start()
    thread2.start()


def receive_messages(client):
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            msg = client.recv(2048).decode('utf-8')
            if msg:
                print(msg + '\n')
        except:
            print('\nNão foi possível permanacer conctado no servidor!\n')
            print('Precione <ENTER> para continuar...')
            client.close()
            break


def send_messages(client, username, message=None):
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            if message:
                client.send(f'<{username}> {message}'.encode('utf-8'))
                message = None
        except Exception as e:
            return


##############  ALL ###################


def close_theads():
    while True:
        global stop_threads
        if stop_threads:
            break
        try:
            if keyboard.is_pressed('esc'):  # if key 'esc' is pressed
                print('Closing (maybe is required you to press ENTER to finish)')
                stop_threads = True
        except:
            pass


def run_champ():
    contador = 0
    while True:
        global stop_threads
        global trigger_send_msg
        if stop_threads:
            break
        time.sleep(10)
        contador += 1
        time_ganhador.append('Random ' + str(contador))
        trigger_send_msg = True


thread_close = threading.Thread(target=close_theads)
thread_server = threading.Thread(target=server_main)

thread_champ = threading.Thread(target=run_champ)
thread_client = threading.Thread(target=client_main, args=[None, 7777])
thread_client2 = threading.Thread(target=client_main, args=[None, 7777])


thread_close.start()
time.sleep(2)
thread_server.start()
time.sleep(2)
thread_client.start()

thread_champ.start()
time.sleep(15)
thread_client2.start()

thread_server.join()
thread_client.join()
print('Finished')
