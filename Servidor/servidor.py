import socket, threading, sys, lib_servidor, requests

lib_servidor.checagem_diretorios()

lista_clientes = []
lista_addr = []

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        url = "https://raw.githubusercontent.com/PauloDoMonte/Zhitkur/main/ip.txt"
        r = requests.get(url,allow_redirects=True)
        open('url.txt','wb').write(r.content)
        arquivo = open('url.txt','r')
        url = arquivo.readline()
        r0 = str(url)
        r1 = r0.split(",")
        Ip = "127.0.0.1"
        Porta = int(r1[1])
        os.remove('url.txt')

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

    except:
        time.sleep(60*1)
        print("Sem acesso a internet")
