from socket import *

cliente = socket(AF_INET, SOCK_STREAM)

host = "0.0.0.0"

porta = 8080

cliente.connect((host, porta))

sentence = input("Digite algo em letra minúscula: ")

sen = sentence.encode()

cliente.send(sen)

dados = cliente.recv(1024)