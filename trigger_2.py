import re
import ast
import main

import time
import socket
import threading

from random import randint

############## DADOS DA PARTIDA ###################

timeA = ["TimeA", 0, 0]
timeB = ["TimeB", 0, 0]
timeC = ["TimeC", 0, 0]
timeD = ["TimeD", 0, 0]
timeE = ["TimeE", 0, 0]
timeF = ["TimeF", 0, 0]

classificacao = [timeA, timeB, timeC, timeD, timeE, timeF]
historicoPartida = []

partidas = [[timeA, timeB], [timeC, timeD], [timeE, timeF], [timeA, timeC]]
partidas_rodando = []

trigger_send_msg = False
trigger_send_msg_finished_game = False
start_champ = False

############## SERVER ###################

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

clients = []
servers_conectados = [('192.168.0.72', 7777)]
error_on_server = False
first_exec_connect = True


def server_main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        server.bind((IPAddr, 7777))
        server.listen()
    except Exception as e:
        return print('\nNão foi possível iniciar o servidor!\n' + str(e))

    while True:
        client, addr = server.accept()
        clients.append(client)
        thread = threading.Thread(target=messages_treatment, args=[client])
        thread.start()


def messages_treatment(client):
    while True:
        try:
            msg = client.recv(2048)
            if 'Me mande a chave + lista de clientes' in str(msg):
                msg = re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(msg))[0]
                global servers_conectados
                if msg and (msg, 7777) not in servers_conectados:
                    servers_conectados.append((msg, 7777))
                update_chave(('Times jogando:' + str(partidas_rodando)).encode('utf-8'), client)
                update_chave(('Updating:' + str([classificacao, historicoPartida, partidas, timeA, timeB, timeC, timeD, timeE, timeF])).encode('utf-8'), client)
                update_chave(('Servidores:' + str(servers_conectados)).encode('utf-8'), client)
                broadcast(('Servidores:' + str(servers_conectados)).encode('utf-8'), client)
            else:
                broadcast(msg, client)
        except Exception as e:
            raise e
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


############## CLIENT ###################


def client_main(ip, host):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        if ip:
            client.connect((ip, host))  # CONNECT TO FIRST EXEC
        else:
            client.connect(('localhost', host))
    except Exception as e:
        global error_on_server
        error_on_server = True
        return print('\nNao foi possível se conectar ao servidor\n')
    time.sleep(3)
    username = str(randint(0, 100))

    global first_exec_connect
    global start_champ
    if first_exec_connect:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        request = f'Me mande a chave + lista de clientes:{IPAddr}'
        first_exec_connect = False
        start_champ = True
    else:
        request = None

    print(f'\n{username} - Conectado!')

    thread1 = threading.Thread(target=receive_messages, args=[client])
    thread2 = threading.Thread(target=send_messages, args=[client, username, request])

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


def receive_messages(client):
    while True:
        global classificacao
        global historicoPartida
        global partidas
        global timeA
        global timeB
        global timeC
        global timeD
        global timeE
        global timeF
        try:
            msg = client.recv(2048).decode('utf-8')
            if msg:
                global partidas_rodando
                global servers_conectados
                if 'Times jogando:' in msg:
                    msg = str(msg).strip('Times jogando:')
                    temporary = ast.literal_eval(msg)
                    for temp in temporary:
                        if temp not in partidas_rodando:
                            partidas_rodando.append(temp)
                    print(f'Atualização "Actual teams" {socket.gethostname()}: ' + str(partidas_rodando) + '\n')
                elif 'Finished:' in msg:
                    msg = str(msg).strip('Finished:')
                    temporary = ast.literal_eval(msg)
                    ##### BEFORE CLASSIFICATION ####
                    classificacao = temporary[0]
                    historicoPartida = temporary[1]
                    partidas = temporary[2]
                    timeA = temporary[3]
                    timeB = temporary[4]
                    timeC = temporary[5]
                    timeD = temporary[6]
                    timeE = temporary[7]
                    timeF = temporary[8]
                    for pr in partidas_rodando:
                        if pr[1] == temporary[9]:
                            partidas_rodando.remove(pr)
                            break
                    print(f'Atualização "Finished" {socket.gethostname()}: ' + str(partidas_rodando) + '\n')
                elif 'Updating:' in msg:
                    msg = str(msg).strip('Updating:')
                    temporary = ast.literal_eval(msg)
                    ##### BEFORE CLASSIFICATION ####
                    classificacao = temporary[0]
                    historicoPartida = temporary[1]
                    partidas = temporary[2]
                    timeA = temporary[3]
                    timeB = temporary[4]
                    timeC = temporary[5]
                    timeD = temporary[6]
                    timeE = temporary[7]
                    timeF = temporary[8]
                    print(f'Atualização "updating" {socket.gethostname()}: ' + str(partidas_rodando) + '\n')
                else:
                    msg = str(msg).strip('Servidores:')
                    temporary = ast.literal_eval(msg)
                    for temp in temporary:
                        if temp not in servers_conectados:
                            servers_conectados.append(temp)
                    print(f'Atualização {socket.gethostname()}:' + str(servers_conectados) + '\n')
        except SyntaxError:
            pass
        except Exception as e:
            print('\nNão foi possível permanacer conctado no servidor!\n')
            print('Precione <ENTER> para continuar...')
            print(e)
            global error_on_server
            error_on_server = True
            # client.close()
            # break
            raise e


def send_messages(client, username, message=None):
    while True:
        try:
            global trigger_send_msg
            global trigger_send_msg_finished_game
            global IPAddr
            if message:
                client.send(f'<{username}> {message}'.encode('utf-8'))
                message = None
            elif trigger_send_msg:
                message = 'Times jogando:' + str(partidas_rodando)
                client.send(message.encode('utf-8'))
                trigger_send_msg = False
                message = None
            elif trigger_send_msg_finished_game:
                message = 'Finished:' + str([classificacao, historicoPartida, partidas, timeA, timeB, timeC, timeD, timeE, timeF, IPAddr])
                client.send(message.encode('utf-8'))
                trigger_send_msg_finished_game = False
                message = None
        except Exception as e:
            return


##############  ALL ###################

def run_champ():
    while True:
        global start_champ
        global trigger_send_msg
        global trigger_send_msg_finished_game
        global timeA
        global timeB
        global timeC
        global timeD
        global timeE
        global timeF

        if start_champ:
            for p in partidas:
                not_running_bool = True
                for pr in partidas_rodando:
                    if p == pr[0]:
                        not_running_bool = False

                if not_running_bool:
                    global classificacao
                    global IPAddr
                    partidas_rodando.append((p, IPAddr))
                    trigger_send_msg = True
                    original_p = p
                    p[0], p[1], classificacao = main.realizaPartida(p, p[0], p[1], classificacao, historicoPartida)
                    for xp in p:
                        if xp[0] == 'TimeA':
                            timeA = xp
                        if xp[0] == 'TimeB':
                            timeB = xp
                        if xp[0] == 'TimeC':
                            timeC = xp
                        if xp[0] == 'TimeD':
                            timeD = xp
                        if xp[0] == 'TimeE':
                            timeE = xp
                        if xp[0] == 'TimeF':
                            timeF = xp

                    print('Finished: ' + str(p))
                    partidas_rodando.remove((p, IPAddr))
                    partidas.remove(original_p)
                    trigger_send_msg_finished_game = True
                    break


thread_champ = threading.Thread(target=run_champ)
thread_server = threading.Thread(target=server_main)
thread_server.start()
thread_champ.start()

time.sleep(1)
for server in servers_conectados:
    thread_client = threading.Thread(target=client_main, args=[server[0], server[1]])
    thread_client.start()
    thread_client.join()
    if not error_on_server:
        break
    error_on_server = False

print('Finished')
