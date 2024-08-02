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
        print(mensagem)
def mensagem_a_enviada(cliente):
    while True:
        mensagem = input()
        cliente.send(mensagem.encode())
print("Hello")
receber = threading.Thread(target=mensagem_a_recebida, args=(cliente,))
receber.start
enviar = threading.Thread(target=mensagem_a_enviada, args=(cliente,))
enviar.start
print("Hello")

cliente.close()
