import socket
import threading

clients = []
usernames = {}

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    
    client_socket.send("Enter your username: ".encode())
    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username
    clients.append(client_socket)
    
    broadcast(f"{username} has joined the chat!".encode())
    
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(message, username + ": ")
            else:
                remove_client(client_socket)
                break
        except:
            continue

def broadcast(message, prefix=""):
    for client in clients:
        client.send(prefix.encode() + message)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        username = usernames.pop(client_socket, None)
        if username:
            broadcast(f"{username} has left the chat.".encode())

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8000))
    server_socket.listen()
    print("[SERVER STARTED] Listening on port 8000.")

    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    start_server()

