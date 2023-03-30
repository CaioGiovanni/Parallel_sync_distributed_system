import ast
import time
import socket
import threading

from random import randint

time_ganhador = []
trigger_send_msg = False
time_ganhador_atualizado = []

##############  SERVER ###################


clients = []
servers_conectados = [('localhost', 7777)]
first_exec_connect = True


def server_main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7777))
        server.listen()
    except Exception as e:
        return print('\nNão foi possível iniciar o servidor!\n' + str(e))

    while True:
        client, addr = server.accept()
        clients.append(client)
        thread = threading.Thread(target=messages_treatment, args=[client])
        thread.start()


# def send_updates_to_clients(clients):
#     while True:
#         global trigger_send_msg
#         if trigger_send_msg:
#             broadcast(str(time_ganhador).encode('utf-8'), clients)
#             trigger_send_msg = False


def messages_treatment(client):
    while True:
        try:
            msg = client.recv(2048)
            if 'Me mande a chave + lista de clientes' in str(msg):
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

    global first_exec_connect
    if first_exec_connect:
        request = 'Me mande a chave + lista de clientes'
        first_exec_connect = False

    else:
        request = None

    print(f'\n{username} - Conectado!')

    thread1 = threading.Thread(target=receive_messages, args=[client])
    thread2 = threading.Thread(target=send_messages, args=[client, username, request])

    thread1.start()
    thread2.start()


def receive_messages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if msg:
                global time_ganhador_atualizado
                time_ganhador_atualizado = ast.literal_eval(msg)
                print('Atualização: ' + str(time_ganhador_atualizado) + '\n')
        except Exception as e:
            print('\nNão foi possível permanacer conctado no servidor!\n')
            print('Precione <ENTER> para continuar...')
            print(e)
            client.close()
            break


def send_messages(client, username, message=None):
    while True:
        try:
            if message:
                client.send(f'<{username}> {message}'.encode('utf-8'))
                message = None
        except Exception as e:
            return


##############  ALL ###################

def run_champ():
    contador = 0
    while True:
        global trigger_send_msg
        time.sleep(1)
        contador += 1
        time_ganhador.append('Random ' + str(contador))
        trigger_send_msg = True


thread_server = threading.Thread(target=server_main)

thread_champ = threading.Thread(target=run_champ)
thread_client = threading.Thread(target=client_main, args=[None, 7777])
# thread_client2 = threading.Thread(target=client_main, args=[None, 7777])


thread_champ.start()
thread_server.start()
time.sleep(5)
thread_client.start()

# time.sleep(15)
# thread_client2.start()

thread_server.join()
thread_client.join()
print('Finished')
