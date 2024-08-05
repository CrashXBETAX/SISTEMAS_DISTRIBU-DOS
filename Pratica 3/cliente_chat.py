from socket import *
import sys
import threading

user = sys.argv[1]

cliente = socket(AF_INET, SOCK_STREAM)

host = "0.0.0.0"
porta = 8080

cliente.connect((host, porta))

cliente.send(user.encode())

def mensagem_a_recebida(cliente):
    while True:
        dados = cliente.recv(1024)
        mensagem = dados.decode()
        if not mensagem:
            continue
        if mensagem == "Conexão encerrada pelo servidor":
            cliente.close()
            print("Encerrando conexão")
            break
        else:
            print(mensagem)
        
def mensagem_a_enviada(cliente):
    while True:
        mensagem = input()
        if not mensagem:
            continue
        if mensagem == "EXIT":
            print("Mensagem 'EXIT' enviada, aguardando desconexão...")
            cliente.send(mensagem.encode())
            break
        else:
            cliente.send(mensagem.encode())

thread_enviada = threading.Thread(target=mensagem_a_enviada, args=(cliente,))
thread_recebida = threading.Thread(target=mensagem_a_recebida, args=(cliente,))

thread_recebida.start()
thread_enviada.start()
