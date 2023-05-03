import socket

HOST = 'localhost' 
PORTA = 5000        


def iniciaCliente():
	sock = socket.socket()
	sock.connect((HOST, PORTA)) 
	return sock

def fazRequisicoes(sock):
	while True:
		if msg == 'fim': break
		sock.send(bytes(msg, 'utf-8'))
		msg = sock.recv(1024) 	
		print(str(msgR,  encoding='utf-8'))
	sock.close() 


def main():
	sock = iniciaCliente()
	fazRequisicoes(sock)


main()