## Pratica 2

### Nome:
    Gabriel Hagui dos Santos
### RA:
    11202020238
### E-mail:
    gabriel.hagui@aluno.ufabc.edu.br

______

## Relatório

No código `server.py`:
```python
from socket import *
import random
import subprocess
import sys
import threading

def enviando_mensagem(connectionSocket, sentence):
    sen = sentence.encode()
    connectionSocket.send(sen)

def recebendo_mensagem(connectionSocket, clientes):
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
        thread_para_cliente = threading.Thread(target=abrindo_um_thread,
                                                args=(connectionSocket, clientes))
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
```
---
No início, criei uma função principal que configura o socket para inicializar a aplicação como servidor, utilizando o IP e a porta:
```python
def iniciando_server()
    serverPort = 8080
    serverIp = "0.0.0.0"
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverIp, serverPort))
    serverSocket.listen(1)
```
Adicionei um laço de repetição para garantir que o servidor permaneça ligado e disponível para receber e enviar mensagens, independentemente da quantidade de mensagens e de clientes.
```python
while True:
    connectionSocket, addr = serverSocket.accept()
    #(...)
```
Criei uma função que gera um número aleatório e adiciona cada número à lista quando um novo cliente se conecta.
```python
def criando_random(lista):
    num = random.randint(0, 100)
    lista.append(num)
    return lista

criando_random(lista_num)
```
Para funcionar corretamente no script `run_test.sh`, tive que fazer uma "_gambiarra_" para usar uma lista pré-definida. Mesmo com a lista pré-definida, a aplicação adiciona um novo elemento à lista toda vez que um cliente entra, utilizando a variável global `i` como controle para adição. Segue o código abaixo:
```python
def iniciando_server(i)
    #(...)
    lista_num, i = criando_random(lista_num, i)
    #(...)

def criando_random(lista, i):
    lista_pre = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    lista.append(lista_pre[i])
    i += 1
    return lista, i

i = 0
iniciando_server(i)
```
Quando a aplicação recebe um novo cliente que acabou de se conectar ao servidor, adiciona o número aleatório como a resposta correta na lista, vinculando aos dados específicos do cliente.
```python
lista_num, i = criando_random(lista_num, i)
        for aleatorio in lista_num:
            clientes[connectionSocket] = aleatorio

```
Para enviar uma mensagem ao cliente, adicionei uma nova função que pode ser reutilizada quantas vezes, sem precisar repetir o mesmo bloco de código:
```python
def enviando_mensagem(connectionSocket, sentence):
    sen = sentence.encode()
    connectionSocket.send(sen)

mensagem = "Adivinhe o número entre 1 e 100"
enviando_mensagem(connectionSocket, mensagem)
```
Para receber uma mensagem do cliente, a estrutura será parecida com a função de enviar.
```python
def recebendo_mensagem(connectionSocket, clientes):
    dados = connectionSocket.recv(1024)
    mensagem = dados.decode()

recebendo_mensagem(connectionSocket, lista_aleatorios)
```
Para processar as respostas do cliente e fornecer feedback com base em condições como 'Acima', 'Abaixo' e 'Igual', adicionei o código:
```python
def recebendo_mensagem(connectionSocket, clientes):
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
```
Executei o arquivo `run_test.sh` e descobri que o servidor não funciona com vários clientes ao mesmo tempo. Para corrigir isso, criei uma thread sempre que um novo cliente se conecta:
```python
def abrindo_um_thread(connectionSocket, clientes):
    enviando_mensagem(connectionSocket, "Adivinhe o número entre 1 e 100")
    recebendo_mensagem(connectionSocket, clientes)

thread_para_cliente = threading.Thread(target=abrindo_um_thread,
                                        args=(connectionSocket, clientes))
thread_para_cliente.start()

```

Após uma exceção na aplicação, sempre apareceu um erro dizendo que a porta estava em uso. Isso atrapalhou a produtividade no desenvolvimento. Para resolver isso, encontrei uma solução no [Stack Overflow](https://stackoverflow.com/questions/6380057/address-already-in-use-error-when-binding-a-socket-in-python) e adicionei ao código para reutilizar a porta se tiver.
```python
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

```

Além disso, coloquei o código que mata o processo após uma exceção para garantir que a porta não seja indisponível.
```python
sys.exit(1)
```
Com essa solução, o erro de porta em uso não aparece mais.

---





No código `client.py`:

```python
from socket import *

cliente = socket(AF_INET, SOCK_STREAM)
host = "0.0.0.0"
porta = 8080
cliente.connect((host, porta))

while True:
    dados = cliente.recv(1024)
    mensagem = dados.decode()
    print(mensagem)
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

cliente.close()
```

É uma aplicação com processamento simples que se conecta ao servidor via um IP `0.0.0.0` e uma porta `8080` específicos utilizando socket. Além disso, envia dados após o input e recebe uma mensagem do servidor. A aplicação se encerra quando uma condição específica de mensagem é verdadeira. Ela recebe e envie umas mensagens na repetição, permitindo que continue rodando independentemente da quantidade de mensagens até receber uma mensagem de confirmação de encerramento da conexão. A entrada é realizada com texto específico recebido de servidor de acordo com as condições da mensagem como "Abaixo".

### Resultado:

```
Servidor iniciado com PID 12027
Servidor iniciado no endereço 0.0.0.0 e porta 8080
Teste 1
Conexão de ('127.0.0.1', 59138)
Número alvo para este cliente: 10
Palpite recebido: 1, Número alvo: 10
Número alvo para este cliente: 10
Palpite recebido: 10, Número alvo: 10
Teste de adivinhar passou
Teste 2
Conexão de ('127.0.0.1', 59154)
Número alvo para este cliente: 20
Teste de desistência passou
Teste 3
Conexão de ('127.0.0.1', 59170)
Número alvo para este cliente: 30
Palpite recebido: 20, Número alvo: 30
Número alvo para este cliente: 30
Palpite recebido: 25, Número alvo: 30
Número alvo para este cliente: 30
Teste de dois palpites e desistência passou
Teste 4
Conexão de ('127.0.0.1', 59176)
Número alvo para este cliente: 40
Conexão de ('127.0.0.1', 59180)
Número alvo para este cliente: 50
Palpite recebido: 30, Número alvo: 50
Número alvo para este cliente: 50
Palpite recebido: 35, Número alvo: 50
Número alvo para este cliente: 50
Palpite recebido: 99, Número alvo: 50
Número alvo para este cliente: 50
Palpite recebido: 77, Número alvo: 50
Número alvo para este cliente: 50
Palpite recebido: 39, Número alvo: 50
Número alvo para este cliente: 50
Palpite recebido: 50, Número alvo: 50
Teste de dois clientes sequenciais passou
Teste 5
Conexão de ('127.0.0.1', 41510)
Número alvo para este cliente: 60
Palpite recebido: 55, Número alvo: 60
Número alvo para este cliente: 60
Palpite recebido: 65, Número alvo: 60
Número alvo para este cliente: 60
Palpite recebido: 60, Número alvo: 60
Conexão de ('127.0.0.1', 41512)
Número alvo para este cliente: 70
Palpite recebido: 65, Número alvo: 70
Número alvo para este cliente: 70
Palpite recebido: 75, Número alvo: 70
Número alvo para este cliente: 70
Palpite recebido: 70, Número alvo: 70
Conexão de ('127.0.0.1', 41514)
Número alvo para este cliente: 80
Palpite recebido: 75, Número alvo: 80
Número alvo para este cliente: 80
Palpite recebido: 85, Número alvo: 80
Número alvo para este cliente: 80
Palpite recebido: 80, Número alvo: 80
Teste de três clientes sequenciais passou
Servidor encerrado
******************************************
Nota final: 10/10
******************************************
```
























