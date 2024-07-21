## Pratica 1

### Nome:
    Gabriel Hagui dos Santos
### RA:
    11202020238
### E-mail:
    gabriel.hagui@aluno.ufabc.edu.br

______

## Relatório

**Modifique os tempos de espera e observe como isso afeta a troca de mensagens**

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

A segunda linha da imagem acima mostra que o código Python importa a biblioteca __time__. Em seguida, as linhas 7 e 14 utilizam a função __sleep__ da biblioteca __time__, que é responsável por causar um "atraso" em segundos. No código, duas threads são lançadas ao mesmo tempo: __send_message__ e __receive_messages__. Pensando sobre isso, se __send_message__ demorar muito para enviar enquanto __receive_messages__ funciona sem atraso, como isso afetaria o funcionamento? Modifiquei a linha 7:
```python
time.sleep(random.randint(1,5)) -> time.sleep(10)
```

Modiquei a linha 14:
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

Executei o código. O código está funcionando bem mesmo que a função __send__message__ demora 10 segundos a enviar e a função __receive__messages__exibe uma mensagem quando tiver na lista de ____messages____. Porém na trás do sistema, a função __receive__messages__ está rodando muitas vezes aguardando por uma mensagem. Modifiquei abaixo:
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
Com a modificação acima, observa que o funcionamento é similar ao dos sistemas distribuídos. Assim, a aplicação, como cliente, fica no aguardo de uma mensagem, por exemplo, e-mail do servidor.

No outro experimento, a função __send_message__ é extremamente rápida, porém __receive_messages__ tem um maior atraso, como 10 segundos.

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

Pelo output acima, apresenta grande gargalo, pois o processo 1 envia 19 mensagens, mas o processo 2 recebeu e exibiu apenas uma mensagem a cada 10000 ms. Assim, isso acaba gerando um resultado mais negativo do que no primeiro experimento.

___

__Implemente um mecanismo de controle de fluxo para evitar que a lista de mensagens cresça indefinidamente.__

Pensando sobre isso, o controle de fluxo requer um limite para a fila de mensagens. Quando o processo atinge a quantidade máxima de mensagens, escolhi que seja 16 mensagens e um atraso de 16 segundos. Durante esse tempo, a função __receive_messages__ sofre com grande gargalo e alta latência, fazendo o __pop__ das mensagens lentamente. Quando os 16 segundos acabam, as mensagens voltam a ser enviadas até atingir novamente 16 mensagens. O processo se repete.

* Primeiro determinei uma variável de limite de mensagens que é __max_messages__
* Adicionei a linha __if len(messages) < max_messages:__ para ter controle de fluxo
* Adicionei uma condição quando a quantidade máxima é atingida, que aciona o __sleep__ de 16 segundos.

No código:

```python
import threading
import time
import random

def send_message(process_id, messages, max_messages):
    contador = 1
    while True:
        if len(messages) < max_messages:
            time.sleep(0)
            message = f"Mensagem do processo {process_id}"
            messages.append(message + f" - {contador}")
            print(f"Processo {process_id} enviou: {message} - {contador}")
            contador += 1
        else:
            print("Fila cheia! Aguardando...")
            time.sleep(16)

def receive_messages(process_id, messages, max_messages):
    while True:
        time.sleep(random.randint(0,5))
        if messages:
            message = messages.pop(0)
            print(f"Processo {process_id} recebeu: {message}")
        else:
            print("Aguardando")

messages = []
max_messages = 16

sender_thread = threading.Thread(target=send_message, args=(1, messages, max_messages))
receiver_thread = threading.Thread(target=receive_messages, args=(2, messages, max_messages))

sender_thread.start()
receiver_thread.start()

sender_thread.join()
receiver_thread.join()
```
Output:
```
Processo 1 enviou: Mensagem do processo 1 - 1
Processo 1 enviou: Mensagem do processo 1 - 2
Processo 1 enviou: Mensagem do processo 1 - 3
Processo 1 enviou: Mensagem do processo 1 - 4
Processo 1 enviou: Mensagem do processo 1 - 5
Processo 1 enviou: Mensagem do processo 1 - 6
Processo 1 enviou: Mensagem do processo 1 - 7
Processo 1 enviou: Mensagem do processo 1 - 8
Processo 1 enviou: Mensagem do processo 1 - 9
Processo 1 enviou: Mensagem do processo 1 - 10
Processo 1 enviou: Mensagem do processo 1 - 11
Processo 1 enviou: Mensagem do processo 1 - 12
Processo 1 enviou: Mensagem do processo 1 - 13
Processo 1 enviou: Mensagem do processo 1 - 14
Processo 1 enviou: Mensagem do processo 1 - 15
Processo 1 enviou: Mensagem do processo 1 - 16
Fila cheia! Aguardando...
Processo 2 recebeu: Mensagem do processo 1 - 1
Processo 2 recebeu: Mensagem do processo 1 - 2
Processo 2 recebeu: Mensagem do processo 1 - 3
Processo 2 recebeu: Mensagem do processo 1 - 4
Processo 2 recebeu: Mensagem do processo 1 - 5
Processo 1 enviou: Mensagem do processo 1 - 17
Processo 1 enviou: Mensagem do processo 1 - 18
Processo 1 enviou: Mensagem do processo 1 - 19
Processo 1 enviou: Mensagem do processo 1 - 20
Processo 1 enviou: Mensagem do processo 1 - 21
Fila cheia! Aguardando...
Processo 2 recebeu: Mensagem do processo 1 - 6
Processo 2 recebeu: Mensagem do processo 1 - 7
Processo 2 recebeu: Mensagem do processo 1 - 8
```
---
__Permita que os processos enviem diferentes tipos de mensagens (por exemplo, mensagens de erro, mensagens de controle).__

Pensei em usar a __classe__ do conteúdo da Programação Orientada a Objetos para agrupar vários dados em um único objeto. Isso me lembra das camadas de TCP e HTTP.

* Criei uma classe fora das funções para inicializá-la com dois atributos vazios, que são tipo e conteúdo de mensagem.
* Coloquei a classe __class_message__ nos parâmetros das duas funções para ser utilizada.
* Adicionei mais duas condições com um parâmetro de número aleatório para testar os diferentes tipos de mensagem.
* Alterei o código para salvar o tipo e o conteúdo nos atributos corretos ao gerar uma mensagem.
* Alterei o programa para exibir cada atributo.

Código:
```python
import threading
import time
import random

class Message:
    mensagem = None
    tipo = None

def send_message(process_id, messages, max_messages, classe_message):
    contador = 1
    while True:
        if len(messages) < max_messages:
            time.sleep(0)
            num = random.randint(0,1)
            if num == 0:
                classe_message.tipo = "NORMAL"
                classe_message.mensagem = "Mensagem do processo " + str(process_id)
                messages.append(classe_message)
                print(f"Processo {process_id} enviou: {classe_message.tipo} - {classe_message.mensagem}")
                contador += 1
            elif num == 1:
                classe_message.tipo = "ERRO"
                classe_message.mensagem = "404"
                messages.append(classe_message)
                print(f"Processo {process_id} enviou: {classe_message.tipo} {classe_message.mensagem}")
            
        else:
            print("Fila cheia! Aguardando...")
            time.sleep(16)

def receive_messages(process_id, messages, max_messages,classe_message):
    while True:
        time.sleep(random.randint(0,5))
        if messages:
            message = messages.pop(0)
            print(f"Processo {process_id} recebeu: {classe_message.tipo} - {classe_message.mensagem}")
        else:
            print("Aguardando")

messages = []
class_message = Message()
max_messages = 16

sender_thread = threading.Thread(target=send_message, args=(1, messages, max_messages, class_message))
receiver_thread = threading.Thread(target=receive_messages, args=(2, messages, max_messages, class_message))

sender_thread.start()
receiver_thread.start()

sender_thread.join()
receiver_thread.join()
```

---

__Adicione suporte para envio de mensagens para grupos de processos específicos.__

Pensei em adicionar mais um atributo de grupo da mesma forma que criei os dois atributos, tipo e conteúdo.

* Ajustei a classe para adicionar mais um atributo de grupo.
```python
class Message:
    mensagem = None
    tipo = None
    grupo = None
```
* Criei uma função nova que gera uma mensagem para evitar repetição do código ao incluir uma condição com um parâmetro de grupo aleatório.
* Usei alguns serviços da AWS como exemplos dos grupos.
* Alterei o código para imprimir todos os atributos.

O código final

```python
import threading
import time
import random

class Message:
    mensagem = None
    tipo = None
    grupo = None

def gerando_message(process_id, messages, classe_message):
    num = random.randint(0,1)
    if num == 0:
        classe_message.tipo = "NORMAL"
        classe_message.mensagem = "Mensagem do processo " + str(process_id)
        messages.append(classe_message)
        print(f"Processo {process_id} enviou: {classe_message.grupo} - {classe_message.tipo} - {classe_message.mensagem}")
    elif num == 1:
        classe_message.tipo = "ERRO"
        classe_message.mensagem = "404"
        messages.append(classe_message)
        print(f"Processo {process_id} enviou: {classe_message.grupo} - {classe_message.tipo} - {classe_message.mensagem}")

def send_message(process_id, messages, max_messages, classe_message):
    contador = 1
    while True:
        if len(messages) < max_messages:
            time.sleep(0.75)
            num_grupo = random.randint(0,2)
            if num_grupo == 0:
                classe_message.grupo = "EC2"
                gerando_message(process_id, messages, classe_message)
            if num_grupo == 1:
                classe_message.grupo = "S3"
                gerando_message(process_id, messages, classe_message)
            if num_grupo == 2:
                classe_message.grupo = "RDS"
                gerando_message(process_id, messages, classe_message)
            
        else:
            print("Fila cheia! Aguardando...")
            time.sleep(16)

def receive_messages(process_id, messages, max_messages ,classe_message):
    while True:
        time.sleep(random.randint(0,5))
        if messages:
            message = messages.pop(0)
            print(f"Processo {process_id} recebeu: {classe_message.grupo} - {classe_message.tipo} - {classe_message.mensagem}")
        else:
            print("Aguardando")

messages = []
class_message = Message()
max_messages = 16

sender_thread = threading.Thread(target=send_message, args=(1, messages, max_messages, class_message))
receiver_thread = threading.Thread(target=receive_messages, args=(2, messages, max_messages, class_message))

sender_thread.start()
receiver_thread.start()

sender_thread.join()
receiver_thread.join()

```
























