import socket
import threading
import time

def server():
    clients = dict() # Dicionário de clientes
    data_payload = 2048 # O payload máximo de dados para ser recebido em 'uma tacada só'

    def set_standard_socket():
        s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 22222
        s.bind((host, port))
        return s, host, port

    def handle_client(client: socket.socket):
        client.sendall("You are connected to the server".encode("utf-8")) # Confirma que há conexão com o cliente

        # Manda a lista de clientes disponíveis
        def send_client_list(client: socket.socket):
            s = ""
            for key, value in clients:
                if key is client: continue
                s += str(value[1]) + ", "
            if s == "": s = "No one available"
            else: s = f"{s[:-2]}\n"
            client.sendall(s.encode("utf-8"))

        seeing_client_list = False
        decoded = ""

        while True:
            try:
                msg = client.recv(data_payload)
                decoded = msg.decode("utf-8") # Decodifica a mensagem recebida em utf-8
                decoded = msg.strip() # Tira espaços

                if seeing_client_list:
                    if decoded == "c":
                        seeing_client_list = False
                        pass # Cancela

            except Exception as e:
                client.sendall("Error ocurred. You are disconnected".encode("utf-8")) # Informa ao cliente que houve erro
                remove_client(client) # Remove o cliente do dicionário
                print(f"Error at {clients[client][1]}: {str(e)}") # Printa erro no terminal do servidor
                break # Quebra o laço e termina a thread

    def remove_client(client: socket.socket):
        clients.pop(client)
        client.close() # Testar

    s, host, port = set_standard_socket() # Inicia o socket
    print(f"Server started at {host}:{port}")
    s.listen(5) # Espera pela conexão de qualquer cliente
    num_client = 0
    while True:
        client, addr = s.accept()
        num_client += 1
        clients.update({client: [addr, num_client]})
        print(f'Client {num_client} connected. Address: {addr}')

        # Inicia uma nova thread para lidar com as mensagens do cliente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def main():
    server()

if __name__ == "__main__":
    main()