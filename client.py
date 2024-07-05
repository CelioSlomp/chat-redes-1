import socket
import threading

SERVER_HOSTNAME = "prog27" # Nome da máquina do servidor
SERVER_PORT = 22222 # Porta do servidor
DATA_PAYLOAD = 1024 # O payload máximo de dados para ser recebido em 'uma tacada só'

SERVER_COMMANDS_LIST = \
    "Server commands:\n" + \
    "l - see the client list\n" + \
    "e - exit. closes connection\n"

def client():

    def connect_to_server():
        host = socket.gethostbyname(SERVER_HOSTNAME)
        s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        s.connect((host, SERVER_PORT))
        return s, host
    
    def receive_message_from_server(pr_server: socket.socket):
        decoded = ""
        while True:
            msg = pr_server.recv(DATA_PAYLOAD)
            decoded += msg.decode("utf-8")
            if len(msg) < DATA_PAYLOAD:
                break
        return decoded
    
    def connect_to_client(host):
        s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        s.connect((host, SERVER_PORT))
        return s, host


    s, host = connect_to_server() # Inicia o socket
    print(f"Server connected at {host}:{SERVER_PORT}\n")
    print(receive_message_from_server(s)) # 'You are connected to the server'

    print(SERVER_COMMANDS_LIST) # Imprime os comandos e pede ao user a opcao
    option = input().strip()
    s.sendall(option.encode("utf-8"))

    retorno_server = receive_message_from_server(s) # retorno do server sobre a opcao
    if retorno_server == "":
        print("Cliente recusou o contato.")
    else:                                           # caso o cliente aceite a conexao
        retorno_server = retorno_server.split(":")
        nome_client = retorno_server[0]
        conexao_client, ip_client = connect_to_client(retorno_server[1])

        print(f"SERVER >> Conectado com o usuario {nome_client}. IP: {ip_client}")
    


def main():
    client()

if __name__ == "__main__":
    main()