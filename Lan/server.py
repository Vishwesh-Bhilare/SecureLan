import socket
import threading

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 12345      # Any unused port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames.pop(index)
            broadcast(f"{nickname} left the chat.".encode(), client)
            client.close()
            break

def receive():
    print(f"Server is listening on port {PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode(), client)
        client.send("Connected to the server.".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
