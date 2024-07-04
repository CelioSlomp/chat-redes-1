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
        try:
            client.sendall("You are connected to the server".encode("utf-8")) # Confirma que há conexão com o cliente

            # Manda a lista de clientes disponíveis
            def send_client_list():
                s = ""
                for key, value in clients:
                    if key is client: continue
                    s += str(value[1]) + ", "
                if s == "": s = "No one available"
                else: s = f"{s[:-2]}\n"
                client.sendall(s.encode("utf-8"))

            def ask_for_connection(client_number: int):
                for key, value in clients:
                    if key is client: continue
                    if client_number == value[1]:
                        key.sendall("Someone wants to connect to you. Do you accept?".encode("utf-8"))
                        msg = key.recv(data_payload)
                        decoded = msg.decode("utf-8") # Decodifica a mensagem recebida em utf-8
                        decoded = msg.strip() # Tira espaços
                        if decoded == "y":
                            return True, value[0]
                        else:
                            return False, None

            seeing_client_list = False
            decoded = ""

            while True:
                msg = client.recv(data_payload)
                decoded = msg.decode("utf-8") # Decodifica a mensagem recebida em utf-8
                decoded = msg.strip() # Tira espaços

                if seeing_client_list:
                    if decoded == "c": # Cliente cancelou
                        seeing_client_list = False
                        continue
                    else:
                        accepted, addr = ask_for_connection(int(decoded))
                        if accepted:
                            client.sendall(f"Request accepted. Address: {addr}".encode("utf-8"))
                            break # Desconecta o cliente
                        else:
                            client.sendall("Request refused".encode("utf-8"))
                else:
                    if decoded == "l":
                        seeing_client_list = True
                        send_client_list()
                    else: # Cliente cancelou
                        continue 
        except Exception as e:
            try:
                client.sendall("Error ocurred. You are disconnected".encode("utf-8")) # Informa ao cliente que houve erro
            except:
                pass
            remove_client(client) # Remove o cliente do dicionário
            print(f"Error at {clients[client][1]}: {str(e)}") # Printa erro no terminal do servidor

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