#HR Dr. Park's github, in class walkthrough, notes, and github copilot debugger
# Jack Myhre
import socket
import threading
import time

SERVER_IP = '10.14.3.159'
SERVER_PORT = 12345

stop_flag = threading.Event()

# if error() occurs, or 'exit' returns from server, disconnect server and exit
def receive():
    while not stop_flag.is_set():
        try:
            message = client.recv(1024).decode()
            if message == 'exit':
                print('Disconnected from server!')
                stop_flag.set()
                client.close()
                break
            else:
                print(message)
        except:
            print('An error occurred!')
            stop_flag.set()
            client.close()
            break
        


if __name__ == '__main__':

    nickname = input('Choose your nickname: ')

    # create a socket object for client service
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))

    # Send the nickname to the server 
    client.send(nickname.encode())

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    
    while True:
        time.sleep(0.05)
        message = input('>> ')
        if (message == 'exit'):
            client.send(message.encode())
            client.close()
            stop_flag.set()
            receive_thread.join()
            break
        else:
            client.send(f'{nickname} says: {message}'.encode())
