import threading
import time

def recebendo():
    try:
        i = 0
        while True:
            
            s = "cliente 3 >> recebida mensagem de teste"
            print(f"\r{s}", i)

            if i == 10:
                return

            time.sleep(3)
            i += 1
    except:
        return

def enviando():
    print("Agora você está conectado com 'cliente 3'. Você pode enviar mensagens")
    while True:
        s = input()
        print("ENVIADO:", s)

thread_recebendo = threading.Thread(target=recebendo)
thread_enviando = threading.Thread(target=enviando)

thread_enviando.start()
thread_recebendo.start()