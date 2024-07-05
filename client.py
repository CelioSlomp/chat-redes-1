import socket
import threading
import time

SERVER_HOSTNAME = "DESKTOP-5I8TS92" # Nome da máquina do servidor
SERVER_PORT = 22222 # Porta do servidor
DATA_PAYLOAD = 1024 # O payload máximo de dados para ser recebido em 'uma tacada só'

SERVER_COMMAND_LIST = \
    "l - See the client list\n" + \
    "w - Wait for client connection\n" + \
    "e - Exit. Closes connection\n" + \
    "Choose one of the options above\n"

def client():

    def connect_to_server():
        host = socket.gethostbyname(SERVER_HOSTNAME)
        s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        s.connect(('192.168.2.4', SERVER_PORT))
        return s, host
    
    def receive_message_from_server(pr_server: socket.socket):
        decoded = ""
        while True:
            msg = pr_server.recv(DATA_PAYLOAD)
            decoded += msg.decode("utf-8")
            if len(msg) < DATA_PAYLOAD:
                break
        return decoded
    
    def connect_to_client(ip: str, port: int): 
        # TESTAR
        s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        s.connect((ip, port))
        return s
    
    def receive_message_from_client(pr_client: socket.socket):
        pass # TODO

    server, host = connect_to_server() # Inicia a conexão com o servidor
    print(f"Server connected at {host}:{SERVER_PORT}\n")
    print("SERVER >> " + receive_message_from_server(server)) # Deve imprimir 'You are connected to the server'

    other_client_addr = ""
    other_client_port = 0
    other_client_number = 0
    step = 0

    # Etapa 0 -> vendo lista de comandos
    # Etapa 1 -> vendo lista de clientes
    # Etapa 2 -> esperando conexão de alguém
    # Etapa 3 -> vai se conectar a outro cliente
    while True:
        if step == 0: # Está na etapa de ver os comandos do servidor
            print(SERVER_COMMAND_LIST) # Imprime os comandos do servidor
            option = input().strip() # Pede a opção ao usuário

            if (option != "l") and (option != "e") and (option != "w"):
                print("Invalid option")
                continue # Pede a opção novamente ao usuário
            elif option == "w":
                step == 2
            
            server.sendall(option.encode("utf-8")) # Envia a opção para o servidor
            
            decoded = receive_message_from_server(server)
            if decoded == "You are disconnected": # Cliente enviou 'e' e foi desconectado
                print("SERVER >> " + decoded)
                print("Finishing program")
                return
            else: # Cliente enviou 'l' e recebeu a lista dos clientes
                step = 1
                continue
        elif step == 1: # Está na etapa de receber a lista de clientes
            decoded = receive_message_from_server(server) # Lista dos clientes
            client_list = decoded.strip(",")

            while True:
                print("SERVER >> " + decoded)
                print("Choose one of the items above or 'c' to cancel and go back\n")
                option = input().strip() # Pede o número do cliente ao usuário
                if (option not in client_list) and (option != "c"):
                    print("Invalid option")
                    continue # Pede a opção novamente ao usuário
                else:
                    server.sendall(option.encode("utf-8")) # Envia a opção para o servidor
                    print("SERVER >> " + receive_message_from_server(server)) # 'SERVER >> Asking for connection...'
                    other_client_number = int(option)

                    decoded = receive_message_from_server(server) # Aceitação ou recusa
                    if decoded == "Request refused": # Recusado
                        print("SERVER >> " + decoded)
                        step = 0
                        break # Sai deste laço e volta a printar a lista de comandos
                    else: # Aceito. Vem o endereço e a porta do outro cliente
                        decoded = decoded.split(":")
                        other_client_addr = decoded[0]
                        other_client_port = decoded[1]
                        step = 3
                        break
        elif step == 2: # Está na etapa de esperar por conexão de algum outro cliente
            print("Waiting for connetion from other client...")
            decoded = receive_message_from_server(server)

            while True:
                print("SERVER >> " + decoded)
                print("Choose 'y' to accept or 'n' to refuse")
                option = input().strip() # Pede a opção ao usuário
                if (option != "y") and (option != "n"):
                    print("Invalid option")
                    continue
                elif (option == "y"):
                    pass # TODO
                elif (option == "n"):
                    pass # TODO
        elif step == 3: # Está na etapa de se conectar a outro cliente
            break

    other_client = connect_to_client(other_client_addr, other_client_port)
    print(f"Connected to client {other_client_number}. Address: {other_client_addr}, Port: {other_client_port}")

    def recebe_mensagem():
        while True:
            data = other_client.recv(DATA_PAYLOAD)
            if data:
                print(data.decode('utf-8'))

    def envia_mensagem():
        while True:
            print("b")
            mensagem = input(">> ")
            codificada = mensagem.encode('utf-8')
            other_client.sendall(codificada)

    threading.Thread(target=recebe_mensagem)
    threading.Thread(target=envia_mensagem)


def main():
    client()

if __name__ == "__main__":
    main()