import socket
import pickle

HOST = 'localhost' 
PORT = 5000       


def iniciaCliente():
	sock = socket.socket() 
	sock.connect((HOST, PORT)) 
	return sock


def fazRequisicoes(sock):
	#Funcao de requisicao 
	#do cliente para o servidor
	while True: 
		#tosend e uma lista com argumentos
		#que o cliente envia ao servidor
		#os argumentos sao
		# 1. funcionalidade que o cliente deseja
		# 2. chave (de insert ou consulta)
		# 3. valor (no caso de insert de chave)
		tosend =[]

		#Print para informar o cliente das funcionalidades
		#(Interface simples para o cliente)
		msg = input("0 ou fim - encerrar\n1 ou insert - insere no dicionario\n2 ou query - consulta no dicionario\n")

		#Fim termina a conexao cliente servidor
		if msg == 'fim' or msg == '0': break

		#Insert para inserir no dicionario
		elif msg == 'insert' or msg == '1':
			tosend.append(1)
			print("Diga a chave do dicionario: ")
			tosend.append(input())
			print("Diga o valor da chave: ")
			tosend.append(input())

		#Query para consultar dicionario
		elif msg == 'query' or msg == '2':
			tosend.append(2)
			print("Diga a chave do dicionario: ")
			tosend.append(input())

		#Else para caso alguma outra coisa seja digitada
		else:
			print("Comando desconhecido")
			continue

		#Converte a lista de comandos e parametros em bytes
		tosendBytes = pickle.dumps(tosend)
		#Envia para o servidor
		sock.sendall(tosendBytes)

		#Recebe uma mensagem do cliente 
		#Contendo o tamanho da proxima mensagem
		msgLen = int.from_bytes(sock.recv(4), byteorder='big')

		#mensagem iniciada vazia
		msg = b''
		#Enquanto o tamanho da mensagem que recebemos
		#for menor que o tamanho enviado pelo servidor
		#mantemos o loop
		while len(msg) < msgLen:
			#diminuimos a quantidade de bytes
			#restantnes da mensagem
			bytesFaltando = msgLen - len(msg)
			#recebemos e construimos a mensagem com sock.recv
			#se o tamanho de bytes faltando for maior que 1024, recebemos 1024
			#caso contrario, recebemos o que falta
			msg += sock.recv(1024 if bytesFaltando > 1024 else bytesFaltando)

		#printa a mensagem para o cliente
		#pode ser mensagem confirmando a insercao no dicionario
		#ou a resposta da consulta
		print(str(msg, encoding='utf-8'))

	sock.close()


def main():
	sock = iniciaCliente()
	fazRequisicoes(sock)


main()
 
