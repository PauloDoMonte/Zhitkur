import socket,time,lib_cliente

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Ip = "221.1.1.5"
Porta = 3333

cliente.connect((Ip,Porta))
