from socket import *
import random
import subprocess
import sys

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

def iniciando_server():
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
        lista_num = criando_random(lista_num)
        for aleatorio in lista_num:
            clientes[connectionSocket] = aleatorio
        #print(f"Clientes: {clientes}")
        enviando_mensagem(connectionSocket, "Adivinhe o número entre 1 e 100")
        recebendo_mensagem(connectionSocket, clientes)

def criando_random(lista):
    num = random.randint(0, 100)
    lista.append(num)
    #print(f"Números aleatórios gerados: {lista}")
    return lista

try:
    iniciando_server()
except Exception as e:
    #print(f"Erro inesperado: {e}")
    cmd = "fuser -k 8080/tcp"
    subprocess.run(cmd, shell=True)
    sys.exit(1)