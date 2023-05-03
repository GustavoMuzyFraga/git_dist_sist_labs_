import socket
import select
import sys
import multiprocessing

HOST = ''     
PORTA = 5000  

entradas = [sys.stdin]
conexoes = {}

def iniciaServidor():
	sock = socket.socket()
	sock.bind((HOST, PORTA))
	sock.listen(5) 
	sock.setblocking(False)
	entradas.append(sock)
	return sock

def aceitaConexao(sock):
	clisock, endr = sock.accept()
	conexoes[clisock] = endr 
	return clisock, endr

def atendeRequisicoes(clisock, endr):
	while True:
		msg = (str(novoSock.recv(1024),  encoding='utf-8'))
		if not msg:
			print(str(endr) + ': encerrou')
			clisock.close()
			return
		print(str(endr) + ': ' + str(msg, encoding='utf-8'))
		clisock.send(bytes(msg, 'utf-8'))

def main():
	clientes=[]
	sock = iniciaServidor()
	while True:
		r, w, e = select.select(entradas, [], [])
		for pronto in leitura:
			if pronto == sock:
				clisock, endr = aceitaConexao(sock)
				print (str(endr) + ': conectado')
				cliente = multiprocessing.Process(target=atendeRequisicoes, args=(clisock,endr))
				cliente.start()
				clientes.append(cliente)
			elif pronto == sys.stdin:
				if cmd == 'fim':
					for c in clientes:
						c.join()
					sock.close()
					sys.exit()

main()