import socket 

def main():
    ipDestino = "localhost"
    portaDestino = 8082

    while input("Deseja enviar uma mensagem? (S/N): ") == "S":
        print("---------------------------")
        conexao = criarConexao(ipDestino, portaDestino) # Sempre precisa fazer isto.
        print("---------------------------")
        try:
            mensagem = input("Digite a mensagem que deseja enviar: ")
            conexao.sendall(mensagem.encode('utf-8'))
            
            msgRecebida = ""
            qtdRecebida = 0 
            msgEsperada = len(mensagem) 
            while qtdRecebida < msgEsperada: 
                pacote = conexao.recv(16) # Recebe 16 bytes de pacote
                qtdRecebida += len(pacote)
                msgRecebida += pacote.decode('utf-8') # Decodifica para verificacao
                if len(pacote) == 0:
                    break
          
            if msgRecebida == mensagem: # Apenas para feedback do usuario
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