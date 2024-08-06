## Pratica 3

### Nome:
    Gabriel Hagui dos Santos
### RA:
    11202020238
### E-mail:
    gabriel.hagui@aluno.ufabc.edu.br

______

## Relatório

No código `servidor_chat.py`:
```python
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
                enviando_mensagem_para_outros(connectionSocket, 
                f"{usuarios[connectionSocket]}: {mensagem}", usuarios)

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
        thread_para_cliente = threading.Thread(target=abrindo_um_thread, 
        args=(connectionSocket, usuarios, user, addr))
        thread_para_cliente.start()
        

try:
    iniciando_server()
except Exception as e:
    #print(f"Erro inesperado: {e}")
    sys.exit(1)
```
---
No início, reutilizei o código da prática 2 na prática 3.
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
Apaguei algumas linhas do código que não estavam relacionadas ao objetivo da prática 3.
```python
def recebendo_mensagem(connectionSocket, clientes):
    #(...)
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
Apaguei uma função `criando_random` que não é útil para a prática 3.
```python
def criando_random(lista, i):
    #num = random.randint(0, 100)
    lista_pre = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    lista.append(lista_pre[i])
    i += 1
    return lista, i
```
---
Criei uma função que vincula o nome de usuário enviado pelo cliente à lista de usuários quando um novo cliente é recebido. Segue o código abaixo:
```python
def salvando_user(connectionSocket, usuarios, usuario, addr):
    user = usuarios.get(connectionSocket)
    if not user:
        usuarios[connectionSocket] = usuario
        print(usuarios[connectionSocket])
    enviando_mensagem(connectionSocket, f"Conexão estabelecida com o {addr}")
    print(f"Conexão estabelecida com o {addr}")
    recebendo_mensagem(connectionSocket, usuarios, addr)
```
Para o código acima, precisei usar `usuarios.get(connectionSocket)` porque, se não fosse assim, geraria uma exceção não tratada `KeyError` ao tentar buscar uma chave que não existe na lista. Com o método `get`, não ocorre uma exceção, em vez disso, retorna `None`, que pode ser usado na condição para determinar se o usuário não existe. Portanto, vincular apenas novos usuários.

---
Ajustei a função `recebendo_mensagem`
```python
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
                enviando_mensagem_para_outros(connectionSocket,f"{usuarios[connectionSocket]}: 
                                                                    {mensagem}", usuarios)
```
Essa função passou por algumas alterações, incluindo uma nova mensagem de desconexão e a adição de duas novas funções chamadas.

---
Adicionei a nova função `removendo_user(connectionSocket, usuarios)`, que remove um usuário da lista quando o cliente desloga. Sem essa função, uma exceção não tratada `OSError` seria gerada ao tentar enviar uma mensagem para um usuário offline. Com essa função, garantimos que mensagens não sejam enviadas para clientes desconectados.
```python
def removendo_user(connectionSocket, usuarios):
    user = usuarios.get(connectionSocket)
    if user:
        del usuarios[connectionSocket]
```
---
Adicionei a nova função `enviando_mensagem_para_outros`, que envia uma mensagem para todos os clientes, exceto para o que a enviou. A condição é bastante simples:
```python
def enviando_mensagem_para_outros(connectionSocket, sentence, usuarios):
    sen = sentence.encode()
    for user in usuarios:
        if user != connectionSocket:
            user.send(sen)
```
Para o código acima, envia uma mensagem para todos desde que não seja igual que o usuário de remetente.

---
No código `cliente_chat.py`
```python
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
```
Para o código acima, quando o código recebe um argumento do terminal, ele imediatamente informa ao servidor seu usuário, que é então salvo na lista de usuários.
```python
user = sys.argv[1]
cliente = socket(AF_INET, SOCK_STREAM)
host = "0.0.0.0"
porta = 8080
cliente.connect((host, porta))
cliente.send(user.encode())
```

Criei duas funções separadas para enviar e receber mensagens entre o cliente e o servidor. O uso de threads para ambas as funções é obrigatório neste caso, pois permite que ambas funcionem simultaneamente uma exibe o campo de entrada enquanto a outra recebe mensagens de outros clientes na tela sem travar a exibição. Além disso, o uso de um loop também é essencial para verificar constantemente se o servidor enviou mensagens para o cliente.


### Resultado:

```
Iniciando o servidor...
Servidor iniciado no endereço 0.0.0.0 e porta 8080
Servidor está em execução
Iniciando teste 1: Conexão única
Iniciando cliente Cliente 1...
spawn python3 cliente_chat.py Cliente 1
Cliente 1
Conexão estabelecida com o ('127.0.0.1', 41106)
Conexão estabelecida com o ('127.0.0.1', 41106)
Mensagem 'Olá' enviada por Cliente 1
Mensagem recebida de ('127.0.0.1', 41106): Cliente 1: Olá
Olá
Cliente está em execução
Passou no teste 1: Conexão única

****************************************
Iniciando teste 2: Envio de mensagem EXIT
Iniciando cliente Cliente 2...
spawn python3 cliente_chat.py Cliente 2
Cliente 2
Conexão estabelecida com o ('127.0.0.1', 41422)
Conexão estabelecida com o ('127.0.0.1', 41422)
Mensagem 'EXIT' enviada por Cliente 2
EXIT
Mensagem recebida de ('127.0.0.1', 41422): Cliente 2: EXIT
Mensagem 'EXIT' enviada, aguardando desconexão...
Encerrando conexão
Cliente desconectado:  ('127.0.0.1', 41422)
Cliente Cliente 2 terminou a execução
Cliente não está em execução
Passou no teste 2: Envio de mensagem EXIT

****************************************
Iniciando teste 3: Conexão de múltiplos clientes
Iniciando cliente Cliente 3...
spawn python3 cliente_chat.py Cliente 3
Cliente 3
Conexão estabelecida com o ('127.0.0.1', 41428)
Conexão estabelecida com o ('127.0.0.1', 41428)
Mensagem 'Olá do Cliente 3' enviada por Cliente 3
Olá do Cliente 3
Mensagem recebida de ('127.0.0.1', 41428): Cliente 3: Olá do Cliente 3
Cliente 3: Olá do Cliente 3
Iniciando cliente Cliente 4...
spawn python3 cliente_chat.py Cliente 4
Cliente 4
Conexão estabelecida com o ('127.0.0.1', 46108)
Conexão estabelecida com o ('127.0.0.1', 46108)
Mensagem 'Olá do Cliente 4' enviada por Cliente 4
Olá do Cliente 4
Mensagem recebida de ('127.0.0.1', 46108): Cliente 4: Olá do Cliente 4
Cliente 4: Olá do Cliente 4
Cliente 4: Olá do Cliente 4
Iniciando cliente Cliente 5...
spawn python3 cliente_chat.py Cliente 5
Cliente 5
Conexão estabelecida com o ('127.0.0.1', 46124)
Conexão estabelecida com o ('127.0.0.1', 46124)
Mensagem 'Olá do Cliente 5' enviada por Cliente 5
Olá do Cliente 5
Mensagem recebida de ('127.0.0.1', 46124): Cliente 5: Olá do Cliente 5
Cliente 5: Olá do Cliente 5Cliente 5: Olá do Cliente 5
Cliente 5: Olá do Cliente 5

Cliente está em execução
Cliente 3 está em execução
Cliente está em execução
Cliente 4 está em execução
Cliente está em execução
Cliente 5 está em execução
Passou no teste 3: Conexão de múltiplos clientes

****************************************
Iniciando teste 4: Verificação de broadcast de mensagens
Iniciando cliente Cliente 6...
spawn python3 cliente_chat.py Cliente 6
Cliente 6
Conexão estabelecida com o ('127.0.0.1', 49748)
Mensagem 'Broadcast test message' enviada por Cliente 6
Broadcast test message
Conexão estabelecida com o ('127.0.0.1', 49748)
Mensagem recebida de ('127.0.0.1', 49748): Cliente 6: Broadcast test message
Cliente 6: Broadcast test message
Cliente 6: Broadcast test message
Cliente 6: Broadcast test message
Cliente 6: Broadcast test message
Cliente 3 recebeu a mensagem de broadcast
Cliente 4 recebeu a mensagem de broadcast
Cliente 5 recebeu a mensagem de broadcast
Passou no teste 4: Verificação de broadcast de mensagens

****************************************
Iniciando teste 5: Reenvio de mensagens
Iniciando cliente Cliente 7...
spawn python3 cliente_chat.py Cliente 7
Cliente 7
Conexão estabelecida com o ('127.0.0.1', 53272)
Conexão estabelecida com o ('127.0.0.1', 53272)
Mensagem 'Testando reenvio' enviada por Cliente 7
Testando reenvio
Mensagem recebida de ('127.0.0.1', 53272): Cliente 7: Testando reenvio
Cliente 7: Testando reenvio
Cliente 7: Testando reenvio
Cliente 7: Testando reenvio
Cliente 7: Testando reenvio
Cliente 7: Testando reenvio
Cliente 3 recebeu a mensagem de reenvio
Cliente 4 recebeu a mensagem de reenvio
Cliente 5 recebeu a mensagem de reenvio
Passou no teste 5: Reenvio de mensagens

****************************************
Iniciando teste 6: Desconexão e Reconexão
Iniciando cliente Cliente 8...
spawn python3 cliente_chat.py Cliente 8
Cliente 8
Conexão estabelecida com o ('127.0.0.1', 50392)
Conexão estabelecida com o ('127.0.0.1', 50392)
Mensagem 'Olá do Cliente 8' enviada por Cliente 8
Mensagem recebida de ('127.0.0.1', 50392): Cliente 8: Olá do Cliente 8
Olá do Cliente 8
Cliente 8: Olá do Cliente 8
Cliente 8: Olá do Cliente 8
Cliente 8: Olá do Cliente 8
Cliente 8: Olá do Cliente 8Cliente 8: Olá do Cliente 8

Cliente 8: Olá do Cliente 8
Iniciando cliente Cliente 8...
spawn python3 cliente_chat.py Cliente 8
Cliente 8
Conexão estabelecida com o ('127.0.0.1', 56706)Mensagem 'Reconectando Cliente 8' enviada por Cliente 8
Reconectando Cliente 8

Conexão estabelecida com o ('127.0.0.1', 56706)
Mensagem recebida de ('127.0.0.1', 56706): Cliente 8: Reconectando Cliente 8
Cliente 8: Reconectando Cliente 8
Cliente 8: Reconectando Cliente 8
Cliente 8: Reconectando Cliente 8
Cliente 8: Reconectando Cliente 8
Cliente 8: Reconectando Cliente 8Cliente 8: Reconectando Cliente 8

Cliente 8 reconectado e mensagem recebida
Passou no teste 6: Desconexão e Reconexão

****************************************
Encerrando todos os processos...
Testes concluídos.
Removendo arquivos de log...
Cliente Cliente 6 terminou a execução
Cliente Cliente 8 terminou a execução
Cliente Cliente 7 terminou a execução
Cliente Cliente 1 terminou a execução
Cliente Cliente 4 terminou a execução
Cliente Cliente 3 terminou a execução
Cliente Cliente 5 terminou a execução
Arquivos de log removidos.

****************************************
             NOTA FINAL: 10.00
****************************************
```
























