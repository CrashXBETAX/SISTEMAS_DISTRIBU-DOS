from socket import *

cliente = socket(AF_INET, SOCK_STREAM)

host = "0.0.0.0"
porta = 8080

cliente.connect((host, porta))

while True:
    dados = cliente.recv(1024)
    mensagem = dados.decode()
    print(mensagem)
    try:
        if mensagem == "Adivinhe o número entre 1 e 100":
            num = input("Digite seu palpite ou \"QUIT\" para sair: ")
            cliente.send(num.encode())
        if mensagem == "Igual":
            break
        if mensagem == "Abaixo":
            num = input("Digite seu palpite ou \"QUIT\" para sair: ")
            cliente.send(num.encode())
        if mensagem == "Acima":
            num = input("Digite seu palpite ou \"QUIT\" para sair: ")
            cliente.send(num.encode())
        if mensagem == "Conexão encerrada":
            break
    except EOFError as e:
        break

cliente.close()
