from socket import *
import random
import subprocess
import sys
import threading

def salvando_user(connectionSocket, usuarios, usuario):
    user = usuarios.get(connectionSocket)
    if not user:
        usuarios[connectionSocket] = usuario
        print(usuarios[connectionSocket])

def enviando_mensagem(connectionSocket, sentence):
    sen = sentence.encode()
    connectionSocket.send(sen)

def recebendo_mensagem(connectionSocket, usuarios):
    usuarios = usuarios
    dados = connectionSocket.recv(1024)
    mensagem = dados.decode()
    print(f"Número alvo para este cliente: {usuarios[connectionSocket]}")
    print(mensagem) 
    connectionSocket.close()

def abrindo_um_thread(connectionSocket, usuarios, user):
    salvando_user(connectionSocket, usuarios, user)

def iniciando_server():
    serverPort = 8080
    serverIp = "0.0.0.0"
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((serverIp, serverPort))
    serverSocket.listen(1)
    lista_num = []
    usuarios = {}
    print(f"Servidor iniciado no endereço {serverIp} e porta {serverPort}")
    while True:
        connectionSocket, addr = serverSocket.accept()
        user = connectionSocket.recv(1024).decode()
        thread_para_cliente = threading.Thread(target=abrindo_um_thread, args=(connectionSocket, usuarios, user))
        thread_para_cliente.start()
        

try:
    iniciando_server()
except Exception as e:
    #print(f"Erro inesperado: {e}")
    sys.exit(1)