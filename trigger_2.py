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

partidas_1 = [[timeA, timeB], [timeC, timeD], [timeE, timeF]]
partidas_2 = [[timeA, timeC], [timeD, timeE], [timeF, timeB]]
partidas = partidas_1
partidas_rodando = []

trigger_send_msg = False
trigger_send_msg_finished_game = False
start_champ = False
finished_champ = False

############## SERVER ###################

server_host_atual = None
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
                time.sleep(2)
                update_chave(('Updating:' + str([classificacao, historicoPartida, partidas, timeA, timeB, timeC, timeD, timeE, timeF])).encode('utf-8'), client)
                time.sleep(2)
                update_chave(('Servidores:' + str(servers_conectados)).encode('utf-8'), client)
                time.sleep(2)
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
        global start_champ
        global classificacao
        global historicoPartida
        global partidas_rodando
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
                global servers_conectados
                possibilites = ['Times jogando', 'Finished', 'Updating', 'Servidores']
                conected_msgs = dict()
                conected_msgs[possibilites[0]] = None
                conected_msgs[possibilites[1]] = None
                conected_msgs[possibilites[2]] = None
                conected_msgs[possibilites[3]] = None
                conected_msgs_temp = str(msg).split(':')
                if len(conected_msgs_temp) > 2:
                    for i, cm_temp in enumerate(conected_msgs_temp):
                        for possibilite in possibilites:
                            if possibilite in cm_temp:
                                conected_msgs[possibilite] = conected_msgs_temp[i + 1].split(possibilite[0])[0].split(possibilite[1])[0].split(possibilite[2])[0].split(possibilite[3])[0]

                if 'Times jogando:' in msg or conected_msgs[possibilites[0]]:
                    if conected_msgs[possibilites[0]]:
                        msg = conected_msgs[possibilites[0]]
                    msg = str(msg).strip('Times jogando:')
                    temporary = ast.literal_eval(msg)
                    for temp in temporary:
                        if temp not in partidas_rodando:
                            partidas_rodando.append(temp)
                    print(f'Atualização "Actual teams" {socket.gethostname()}: ' + str(partidas_rodando) + '\n')
                    start_champ = True
                if 'Finished:' in msg or conected_msgs[possibilites[1]]:
                    if conected_msgs[possibilites[1]]:
                        msg = conected_msgs[possibilites[1]]
                    msg = str(msg).strip('Finished:')
                    temporary = ast.literal_eval(msg)
                    ##### BEFORE CLASSIFICATION ####
                    historicoPartida = temporary[1]
                    partidas = temporary[2]
                    if timeA[1] < temporary[3][1] or timeA[2] < temporary[3][2]:
                        timeA = temporary[3]
                    if timeB[1] < temporary[4][1] or timeB[2] < temporary[4][2]:
                        timeB = temporary[4]
                    if timeC[1] < temporary[5][1] or timeC[2] < temporary[5][2]:
                        timeC = temporary[5]
                    if timeD[1] < temporary[6][1] or timeD[2] < temporary[6][2]:
                        timeD = temporary[6]
                    if timeE[1] < temporary[7][1] or timeE[2] < temporary[7][2]:
                        timeE = temporary[7]
                    if timeF[1] < temporary[8][1] or timeF[2] < temporary[8][2]:
                        timeF = temporary[8]
                    classificacao = [timeA, timeB, timeC, timeD, timeE, timeF]
                    classificacao = main.exibeClassificacao(classificacao)
                    for pr in partidas_rodando:
                        if pr[1] == temporary[9]:
                            partidas_rodando.remove(pr)
                            break
                    print(f'Atualização partidas "Finished" {socket.gethostname()}: ' + str(partidas) + '\n')
                    print(f'Atualização partidas rodando "Finished" {socket.gethostname()}: ' + str(partidas_rodando) + '\n')
                if 'Updating:' in msg or conected_msgs[possibilites[2]]:
                    if conected_msgs[possibilites[2]]:
                        msg = conected_msgs[possibilites[2]]
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
                    start_champ = True
                if 'Servidores:' in msg or conected_msgs[possibilites[3]]:
                    if conected_msgs[possibilites[3]]:
                        msg = conected_msgs[possibilites[3]]
                    msg = str(msg).strip('Servidores:')
                    temporary = ast.literal_eval(msg)
                    for temp in temporary:
                        if temp not in servers_conectados:
                            servers_conectados.append(temp)
                    print(f'Atualização {socket.gethostname()}:' + str(servers_conectados) + '\n')
        except Exception as e:
            print('\nNão foi possível permanacer conctado no servidor!\n')
            print('Precione <ENTER> para continuar...')
            print(e)
            global error_on_server
            global server_host_atual
            for server_temp in partidas_rodando:
                if server_temp[1] == server_host_atual:
                    partidas_rodando.remove(server_temp)
            error_on_server = True
            # client.close()
            # break
            raise e


def send_messages(client, username, message=None):
    while True:
        try:
            global trigger_send_msg
            global trigger_send_msg_finished_game
            global finished_champ
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

            if finished_champ:
                message = 'Finished:' + str([classificacao, historicoPartida, partidas, timeA, timeB, timeC, timeD, timeE, timeF, IPAddr])
                client.send(message.encode('utf-8'))
                trigger_send_msg_finished_game = False
                message = None
        except Exception as e:
            return


##############  ALL ###################

def run_champ():
    while True:
        global partidas
        global start_champ
        global finished_champ
        global classificacao
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
                    global IPAddr
                    partidas_rodando.append((p, IPAddr))
                    trigger_send_msg = True
                    p[0], p[1] = main.realizaPartida(p, p[0], p[1], historicoPartida)
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
                    classificacao = [timeA, timeB, timeC, timeD, timeE, timeF]
                    classificacao = main.exibeClassificacao(classificacao)

                    print('Finished: ' + str(p))
                    for partida_temp in partidas_rodando:
                        if partida_temp[0][0][0] == p[0][0] and partida_temp[0][1][0] == p[1][0]:
                            partidas_rodando.remove(partida_temp)
                            break
                    for partida_temp in partidas:
                        if partida_temp[0][0] == p[0][0] and partida_temp[1][0] == p[1][0]:
                            partidas.remove(partida_temp)
                            if not partidas:
                                for x_1 in partidas_1:
                                    if partida_temp[0][0] == x_1[0][0] and partida_temp[1][0] == x_1[1][0]:
                                        partidas = partidas_2
                            break
                    trigger_send_msg_finished_game = True
                    # print('Finished partidas para serem jogadas: ' + str(partidas))
                    break
            if partidas_rodando:
                time.sleep(2)
                print('Agurdando finalizar: ' + str(partidas_rodando))
            if not partidas and not partidas_rodando:
                finished_champ = True
                time.sleep(30)
                print('Partidas finalizadas\n')
                print(classificacao)
                break


thread_champ = threading.Thread(target=run_champ)
thread_server = threading.Thread(target=server_main)
thread_server.start()
thread_champ.start()

time.sleep(1)
for server in servers_conectados:
    server_host_atual = server[0]
    thread_client = threading.Thread(target=client_main, args=[server[0], server[1]])
    thread_client.start()
    thread_client.join()
    if not error_on_server:
        break
    error_on_server = False

print('Finished')
