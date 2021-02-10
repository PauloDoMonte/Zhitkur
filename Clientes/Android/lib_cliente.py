import socket,time

def tentar_conectar(cliente,Ip,Porta):
	try:
		cliente.connect((Ip,Porta))
	except:
		time.sleep(60*10)
		tentar_conectar(cliente,Ip,Porta)
