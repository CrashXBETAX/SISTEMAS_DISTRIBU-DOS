from socket import *
import random
import subprocess
import sys
import threading

def enviando_mensagem(connectionSocket, sentence):
    sen = sentence.encode()
    connectionSocket.send(sen)

def recebendo_mensagem(connectionSocket, clientes):
    clientes = clientes
    dados = connectionSocket.recv(1024)
    mensagem = dados.decode()
    print(f"Número alvo para este cliente: {clientes[connectionSocket]}")   
    if mensagem == "QUIT":
        enviando_mensagem(connectionSocket, "Conexão encerrada")
        connectionSocket.close()
    elif mensagem.isnumeric() == True:
        print(f"Palpite recebido: {mensagem}, Número alvo: {clientes[connectionSocket]}")
        if int(mensagem) == int(clientes[connectionSocket]):
            enviando_mensagem(connectionSocket, "Igual")
            connectionSocket.close()
        elif int(mensagem) > int(clientes[connectionSocket]):
            enviando_mensagem(connectionSocket, "Abaixo")
            recebendo_mensagem(connectionSocket, clientes)
        elif int(mensagem) < int(clientes[connectionSocket]):
            enviando_mensagem(connectionSocket, "Acima")
            recebendo_mensagem(connectionSocket, clientes)

def abrindo_um_thread(connectionSocket, clientes):
    enviando_mensagem(connectionSocket, "Adivinhe o número entre 1 e 100")
    recebendo_mensagem(connectionSocket, clientes)

def iniciando_server(i):
    serverPort = 8080
    serverIp = "0.0.0.0"
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((serverIp, serverPort))
    serverSocket.listen(1)
    lista_num = []
    clientes = {}
    print(f"Servidor iniciado no endereço {serverIp} e porta {serverPort}")
    while True:
        connectionSocket, addr = serverSocket.accept()
        print(F"Conexão de {addr}")
        lista_num, i = criando_random(lista_num, i)
        for aleatorio in lista_num:
            clientes[connectionSocket] = aleatorio
            #print(f"Clientes: {clientes}")
        #print(f"Clientes: {clientes}")
        thread_para_cliente = threading.Thread(target=abrindo_um_thread, args=(connectionSocket, clientes))
        thread_para_cliente.start()
        

def criando_random(lista, i):
    #num = random.randint(0, 100)
    lista_pre = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    lista.append(lista_pre[i])
    i += 1
    return lista, i

try:
    i = 0
    iniciando_server(i)
except Exception as e:
    #print(f"Erro inesperado: {e}")
    sys.exit(1)