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