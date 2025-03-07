#HR Dr. Park's github, in class walkthrough, notes, and github copilot debugger
# Jack Myhre
import socket
import threading
import time

SERVER_IP = "10.14.3.159"
SERVER_PORT = 12345

stop_flag = threading.Event()

clients = [] # list of clients connected
nicknames = [] # list of nicknames of clients connected

def clean(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames[index]
        broadcast(f'{nickname} left the chat!'.encode())
        nicknames.remove(nickname)
        client.close()
        print(f'We have {len(clients)} guests')
  
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
            client.send(f'Number of clients: {len(clients)}'.encode())
        except:
            clean(client) 
        

def server_handle(client):
    while not stop_flag.is_set():
        try:
            message = client.recv(1024)
            if message:
                broadcast(message)
            else:
                clean(client)
                break
        except:
            clean(client)
            break


if __name__ == '__main__':
    finish = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen()
        print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            client_conn, address = server.accept()
            print(f"Connected with {str(address)}")

            nickname = client_conn.recv(1024).decode()
            nicknames.append(nickname)
            clients.append(client_conn)

            print(f'Nickname: {nickname} has joined the chat!')
            broadcast(f'{nickname} joined the chat!'.encode())
            print(f'We have {len(clients)} clients')

            thread = threading.Thread(target=server_handle, args=(client_conn,))
            thread.start()
            