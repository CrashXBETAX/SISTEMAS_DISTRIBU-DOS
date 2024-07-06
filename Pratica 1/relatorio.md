## Pratica 1

### Nome:
    Gabriel Hagui dos Santos
### RA:
    11202020238
### E-mail:
    gabriel.hagui@aluno.ufabc.edu.br

______

1. __"Lembre que a troca de mensagens é uma técnica fundamental em sistemas 
distribuídos, permitindo a comunicação eficiente e assíncrona entre 
processos independentemente de sua localização física, e desempenha um 
papel crucial na construção de sistemas distribuídos escaláveis e confiáveis"__

______

2. OK
______
3. Pratica 1/code.py

______
   
4. Relatório

**Modifique os tempos de espera e observe como isso afeta a troca de 
mensagens**

```python
import threading
import time
import random

def send__message(process__id, messages):
    while True:
        time.sleep(random.randint(1,5)))
        message = f"Mensagem do processo {process__id}"
        messages.append(message)
        print(f"Processo {process__id} enviou: {message}")

def receive__messages(process__id, messages):
    while True:
        time.sleep(random.randint(1,5)))
        if messages:
            message = messages.pop(0)
            print(f"Processo {process__id} recebeu: {message}")

messages = []

sender__thread = threading.Thread(target=send__message, args=(1, messages))
receiver__thread = threading.Thread(target=receive__messages, args=(2, messages))

sender__thread.start()
receiver__thread.start()

sender__thread.join()
receiver__thread.join()
```

A segunda linha da imagem acima mostra que o código do Python importa a biblioteca __time__. Em seguida, a linha 7 e 14 apresentam que usam a função __sleep__ da biblioteca __time__, que são responsáveis por causar um "atraso" em segundos. No código, lançam duas threads no mesmo tempo que são __send__message__ e __receive__messages__. No pensamento, se send__message demora muito a enviar, porém receive__messages funciona sem atraso, como afetaria o funcionamento. Modifiquei na linha 7:
```python
time.sleep(random.randint(1,5)) -> time.sleep(10)
```

Modiquei na linha 14:
```python
time.sleep(random.randint(1,5)) -> time.sleep(1)
```

No código:
```python
import threading
import time
import random

def send__message(process__id, messages):
    while True:
        time.sleep(5)
        message = f"Mensagem do processo {process__id}"
        messages.append(message)
        print(f"Processo {process__id} enviou: {message}")

def receive__messages(process__id, messages):
    while True:
        time.sleep(1)
        if messages:
            message = messages.pop(0)
            print(f"Processo {process__id} recebeu: {message}")

messages = []

sender__thread = threading.Thread(target=send__message, args=(1, messages))
receiver__thread = threading.Thread(target=receive__messages, args=(2, messages))

sender__thread.start()
receiver__thread.start()

sender__thread.join()
receiver__thread.join()
```

Executei o código. O código está funcionando bem mesmo que a função ____send__message____ demora 10 segundos a enviar e a função ____receive__messages____exibe uma mensagem quando tiver na lista de ____messages____. Porém na trás do sistema, a função receive__messages está rodando muitas vezes aguardando por uma mensagem. Modifiquei abaixo:
```python
if messages:
    message = messages.pop(0)
    print(f"Processo {process__id} recebeu: {message}")

```
Para

```python
if messages:
    message = messages.pop(0)
    print(f"Processo {process__id} recebeu: {message}")
else:
    print("Aguardando")
```

Output:
```
Aguardando
Aguardando
Aguardando
Aguardando
Processo 1 enviou: Mensagem do processo 1
Processo 2 recebeu: Mensagem do processo 1
Aguardando
Aguardando
Aguardando
Aguardando
Processo 1 enviou: Mensagem do processo 1
Processo 2 recebeu: Mensagem do processo 1
Aguardando
Aguardando
Aguardando
Aguardando
Processo 1 enviou: Mensagem do processo 1
Processo 2 recebeu: Mensagem do processo 1
```
Com modificação acima, apresenta que é mesma forma de funcionamento dos sistemas distribuidos. Assim aplicação como servidor fica no aguardo por uma mensagem de cliente.

No outro experimento, a função  é extremamente rápido, porém receive_messages tem maior atraso como 10 segundos.

Modifiquei abaixo:

```python
import threading
import time
import random

def send_message(process_id, messages):
    while True:
        time.sleep(0.5)
        message = f"Mensagem do processo {process_id}"
        messages.append(message)
        print(f"Processo {process_id} enviou: {message}")

def receive_messages(process_id, messages):
    while True:
        time.sleep(10)
        if messages:
            message = messages.pop(0)
            print(f"Processo {process_id} recebeu: {message}")
        else:
            print("Aguardando")

messages = []

sender_thread = threading.Thread(target=send_message, args=(1, messages))
receiver_thread = threading.Thread(target=receive_messages, args=(2, messages))

sender_thread.start()
receiver_thread.start()

sender_thread.join()
receiver_thread.join()
```
No código acima, na teoria, send_message tem latência de 500ms e receive_messages tem latência de 10000ms.

Executei o código:

Output:
```
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 2 recebeu: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 2 recebeu: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
Processo 1 enviou: Mensagem do processo 1
```























