import socket
import threading
import time


def server():
    clients = [] # Lista de clientes
    data_payload = 2048 # O payload máximo de dados para ser recebido em 'uma tacada só'

    def set_standard_socket():
        s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 22222
        s.bind((host, port))
        return s, host, port

    def handle_client(client: socket.socket):
        while True:
            try:
                msg = client.recv(data_payload)
                # client.send()
            except:
                remove_client(client)
                break

    def remove_client(client: socket.socket):
        clients.remove(client)
        client.close() # Testar

    s, host, port = set_standard_socket() # Inicia o socket
    print(f"Server started at {host}:{port}")
    start_time = time.time()
    s.listen(5) # Espera pela conexão de qualquer cliente
    # i = 0
    while True:
        client, addr = s.accept()
        clients.append(client)
        print(f'Client connected. Address: {addr}')

        # Inicia uma nova thread para lidar com as mensagens do cliente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def main():
    server()

if __name__ == "__main__":
    main()