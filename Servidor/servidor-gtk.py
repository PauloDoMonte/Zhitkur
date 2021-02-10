import socket, threading, sys, lib_servidor
from tkinter import *

lib_servidor.checagem_diretorios()

lista_clientes = []
lista_addr = []

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Ip = "127.0.0.1"
Porta = 3333
servidor.bind((Ip,Porta))
servidor.listen(100)

class Application(Frame):
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack()
        self.msg = Label(self.widget1, text="Zhitkur 0.0.1")
        self.msg["font"] = ("Verdana", 10, "italic","bold")
        self.msg.pack()

        self.sair = Button(self.widget1)
        self.sair["text"] = "Sair"
        self.sair["width"] = 5
        self.sair["command"] = self.widget1.quit
        self.sair.pack()

root = Tk()
Application(root)
root.mainloop()
