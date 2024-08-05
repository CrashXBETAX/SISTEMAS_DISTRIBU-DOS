from socket import *
import sys
import threading

def salvando_user(connectionSocket, usuarios, usuario, addr):
    user = usuarios.get(connectionSocket)
    if not user:
        usuarios[connectionSocket] = usuario
        print(usuarios[connectionSocket])
    enviando_mensagem(connectionSocket, f"Conexão estabelecida com o {addr}")
    print(f"Conexão estabelecida com o {addr}")
    recebendo_mensagem(connectionSocket, usuarios, addr)

def enviando_mensagem(connectionSocket, sentence):
    sen = sentence.encode()
    connectionSocket.send(sen)

def enviando_mensagem_para_outros(connectionSocket, sentence, usuarios):
    sen = sentence.encode()
    for user in usuarios:
        if user != connectionSocket:
            user.send(sen)

def removendo_user(connectionSocket, usuarios):
    user = usuarios.get(connectionSocket)
    if user:
        del usuarios[connectionSocket]

def recebendo_mensagem(connectionSocket, usuarios, addr):
    while True:
        dados = connectionSocket.recv(1024)
        mensagem = dados.decode()
        if not mensagem:
            continue
        else:
            print(f"Mensagem recebida de {addr}: {usuarios[connectionSocket]}: {mensagem}") 
            if mensagem == "EXIT":
                removendo_user(connectionSocket, usuarios)
                enviando_mensagem(connectionSocket, "Conexão encerrada pelo servidor")
                print("Cliente desconectado: ", addr)
                connectionSocket.close()
                break
            else:
                #enviando_mensagem(connectionSocket, f"{usuarios[connectionSocket]}: {mensagem}")
                enviando_mensagem_para_outros(connectionSocket, f"{usuarios[connectionSocket]}: {mensagem}", usuarios)

def abrindo_um_thread(connectionSocket, usuarios, user, addr):
    salvando_user(connectionSocket, usuarios, user, addr)
    

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
        thread_para_cliente = threading.Thread(target=abrindo_um_thread, args=(connectionSocket, usuarios, user, addr))
        thread_para_cliente.start()
        

try:
    iniciando_server()
except Exception as e:
    #print(f"Erro inesperado: {e}")
    sys.exit(1)