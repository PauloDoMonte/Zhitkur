import socket, threading, sys, lib_servidor

lib_servidor.checagem_diretorios()

lista_clientes = []
lista_addr = []

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Ip = "221.1.1.5"
Porta = 3333
servidor.bind((Ip,Porta))
servidor.listen(100)

estado = True

while estado:
    conn, addr = servidor.accept()

    lista_clientes.append(conn)
    lista_addr.append(addr[0])

    lib_servidor.registro_conexoes(conn,addr)

    print("{} se conectou".format(addr[0]))
    if(len(lista_clientes) == 1):
        processo = threading.Thread(target=lib_servidor.painel_controle, args=(lista_addr, lista_clientes))
        processo.start()