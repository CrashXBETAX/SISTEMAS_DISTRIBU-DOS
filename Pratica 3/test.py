import threading
import time

def envia_mensagem():
    time.sleep(5)
    print("TESTE")

def entrada():
    mensagem = input()
    print(mensagem)

threading.Thread(target = entrada, args=()).start()
threading.Thread(target = envia_mensagem, args=()).start()