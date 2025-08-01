import socket
import threading

SERVER_IP = input("Enter server IP: ")  # e.g., 192.168.1.100
PORT = 12345

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("An error occurred. Exiting.")
            client.close()
            break

def write():
    while True:
        msg = f'{nickname}: {input()}'
        client.send(msg.encode())

threading.Thread(target=receive).start()
threading.Thread(target=write).start()
