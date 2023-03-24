import threading
import socket


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nNao foi possível se conectar ao servidor\n')
    username = input('Usuário: ')
    print('\nConectado!')

    thread1 = threading.Thread(target=receive_messages, args=[client])
    thread2 = threading.Thread(target=send_messages, args=[client, username])

    thread1.start()
    thread2.start()


def receive_messages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg + '\n')
        except:
            print('\,Não foi possível permanacer conctado no servidor!\n')
            print('Precione <ENTER> para continuar...')
            client.close()
            break


def send_messages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except Exception as e:
            return


main()
