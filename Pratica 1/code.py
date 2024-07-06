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

