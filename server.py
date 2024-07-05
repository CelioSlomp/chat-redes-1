import socket
import threading
import traceback

SERVER_HOSTNAME = socket.gethostname() # Nome da máquina do servidor
SERVER_PORT = 22222 # Porta do servidor
DATA_PAYLOAD = 1024 # O payload máximo de dados para ser recebido em 'uma tacada só'

STANDARD_CLIENT_PORT = 22223

def server():
    clients = dict() # Dicionário de clientes

    def get_client_by_num(client_number: int):
        for key in clients.keys():
            if clients[key][1] == client_number:
                return key
        return None

    def bind_standard_socket():
        host = socket.gethostbyname(SERVER_HOSTNAME)
        s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        s.bind((host, SERVER_PORT))
        return s, host
    
    def receive_message(pr_client: socket.socket):
        decoded = ""
        while True:
            msg = pr_client.recv(DATA_PAYLOAD)
            decoded += msg.decode("utf-8")
            if len(msg) < DATA_PAYLOAD:
                break
        return decoded

    def handle_client(client: socket.socket):
        try:
            # Confirma que há conexão com o cliente
            client.sendall("You are connected to the server".encode("utf-8"))

            # Manda a lista de clientes disponíveis
            def send_client_list():
                s = ""
                for key in clients.keys():
                    if key is client: continue
                    s += str(clients[key][1]) + ", "
                if s == "": s = "No one available"
                else: s = f"{s[:-2]}"
                client.sendall(s.encode("utf-8"))

            def ask_for_connection(client_requested_num: int):
                client_requested = get_client_by_num(client_requested_num)
                client_requested.sendall(f"Client {clients[client][0]} wants to connect to you. Do you accept?".encode("utf-8"))
                decoded = receive_message(client_requested)
                if decoded == "y": return True, clients[client_requested][1] # Retorna endereço
                else: return False, None

            seeing_client_list = False
            decoded = ""

            while True:
                decoded = receive_message(client)

                if seeing_client_list:
                    if decoded == "c": # Cliente cancelou
                        client.sendall("Returning to command list".encode("utf-8"))
                        seeing_client_list = False
                        continue
                    else:
                        client.sendall("Asking for connection...".encode("utf-8"))
                        accepted, addr = ask_for_connection(int(decoded))
                        if accepted:
                            client.sendall(f"{addr}:{STANDARD_CLIENT_PORT}".encode("utf-8"))
                            break
                        else:
                            client.sendall("Request refused".encode("utf-8"))
                else:
                    if decoded == "l":
                        seeing_client_list = True
                        send_client_list()
                    elif decoded == "e": # Cliente fechou conexão
                        client.sendall("You are disconnected".encode("utf-8"))
                        print(f"Client {clients[client][1]} exited") # Printa que o cliente se desconectou
                        break
            remove_client(client) # Remove o cliente do dicionário 
            return
        except Exception as e:
            # Tenta informar ao cliente que houve erro
            try: client.sendall("Error ocurred. You are disconnected".encode("utf-8"))
            except: pass
            print(f"Error at client {clients[client][1]}: {str(e)}") # Printa erro no terminal do servidor
            traceback.print_stack()
            remove_client(client) # Remove o cliente do dicionário

    def remove_client(client: socket.socket):
        clients.pop(client)
        client.close()

    s, host = bind_standard_socket() # Inicia o socket
    print(f"Server {SERVER_HOSTNAME} started at {host}:{SERVER_PORT}")
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