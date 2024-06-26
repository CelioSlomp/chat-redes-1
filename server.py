import socket
import threading

clients = [] # Lista de clientes
data_payload = 2048 # O payload máximo de dados para ser recebido em 'uma tacada só'
s: socket.socket = None

def set_standard_socket():
    s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 22222
    s.bind((host, port))
    return s, host, port

def handle_client(client):
    while True:
        try:
            msg = client.recv(2048)
        except:
            remove_client(client)
            break

def remove_client(client):
    clients.remove(client)

def server():
    set_standard_socket()
    s.listen() # Espera pela conexão de qualquer cliente
    # i = 0
    while True:
        client, addr = s.accept()
        clients.append(client)
        print(f'Cliente conectado. IP: {addr}')

        # Inicia uma nova thread para lidar com as mensagens do cliente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def close_server():
    s.close()

def main():
    server()

if __name__ == "__main__":
    main()