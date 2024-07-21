from socket import *
import random
import subprocess

def iniciando_server():
    serverPort = 8080
    serverSocket = socket(AF_INET , SOCK_STREAM)
    serverSocket.bind(("0.0.0.0" , serverPort))
    serverSocket.listen(1)
    lista_cliente = []
    lista_num = []
    while True:
        connectionSocket, addr = serverSocket.accept()
        lista_cliente.append(connectionSocket)
        lista_num = criando_random(lista_num)
        sentence = connectionSocket.recv(1024)
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence)
        msg = sentence
        print(msg)
        print(len(lista_cliente))
        connectionSocket.close()

def criando_random(lista):
    num = random.randint(0,100)
    lista.append(num)
    print(lista)
    return lista
    
try:
    iniciando_server()
except Exception as e: 
    print(e)
    cmd = "fuser -k 8069/tcp"
    subprocess.call(cmd)
    quit() 



