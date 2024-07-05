import socket 

server_command_list = \
    "Commands:\n" + \
    "l - see the client list\n" + \
    "e - exit. closes connection\n"

def main():
    ip_destino = "localhost"
    porta_destino = 8082

    while input("Deseja enviar uma mensagem? (S/N): ") == "S":
        print("---------------------------")
        conexao = criarConexao(ip_destino, porta_destino) # Sempre precisa fazer isto.
        print("---------------------------")
        try:
            mensagem = input("Digite a mensagem que deseja enviar: ")
            conexao.sendall(mensagem.encode('utf-8'))
            
            msg_recebida = ""
            qtd_recebida = 0 
            msgEsperada = len(mensagem) 
            while qtd_recebida < msgEsperada: 
                pacote = conexao.recv(16) # Recebe 16 bytes de pacote
                qtd_recebida += len(pacote)
                msg_recebida += pacote.decode('utf-8') # Decodifica para verificacao
                if len(pacote) == 0:
                    break
          
            if msg_recebida == mensagem: # Apenas para feedback do usuario
                print("Mensagem recebida.")
            else:
                print("Mensagem nao recebida. Fechando conexao.")

        except socket.error as e: 
            print ("Erro no socket", e) 
        except Exception as e: 
            print ("Outro erro", e)
        
        print("---------------------------")
    else:
        print("Fechando conexao.")
        conexao.close()

def criarConexao(host, porta):
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Conectando ao IP {host} com porta {porta}")
    conexao.connect((host, porta)) 

    return conexao

if __name__ == "__main__":
    main()