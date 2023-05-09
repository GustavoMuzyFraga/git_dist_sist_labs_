import socket
import select
import sys
import multiprocessing
import pickle


HOST = '' 
PORT = 5000  

entradas = [sys.stdin]
conexoes = {}

#iniciar o manager
manager = multiprocessing.Manager()
#Usamos o manager para controlar
#o dicionario entre varios processos
dictionary = manager.dict()


def iniciaServidor():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(5) 
    sock.setblocking(False)
    entradas.append(sock)
    return sock


def aceitaConexao(sock):
    clisock, endr = sock.accept()
    conexoes[clisock] = endr 
    return clisock, endr


#Funcao de insert 
#insere no dicionario
#e retorna mensagem para o cliente
def insert(clisock,endr, data, lock):

    #Adquirimos um lock para 
    #proteger a integridade do dicionario
    #perante varias requisicoes concorrentes
    lock.acquire()

    #Se a chave ja existe no dicionario,
    #logamos no servidor a tentativa
    #e guardamos a mensagem para enviar ao cliente
    if data[1] in dictionary:    
        print(str(endr)+ ': Tentou inserir chave existente '+ str(data[1]))
        msg = "Chave ja existe, valor nao inserido"

    #Se a chave nao existe no dicionario,
    #inserimos ela
    #e guardamos a mensagem de adicionado para enviar ao cliente
    else:
        dictionary[data[1]]=data[2]
        print(str(endr)+ ': Inseriu nova chave '+ str(data[1])+ ' como o valor ' + str(data[2]))
        msg = "Adicionado"    

    #liberamos o lock
    lock.release() 

    #retorna a mensagem a ser enviada
    return msg


#Funcao de consulta
#consulta o dicionario
#retorna para o cliente o resultado
def query(endr, data):

	#Se a chave consultada estiver no dicionario
	#guarda o resultado para enviar
	#loga uma mensagem no servidor
	if data[1] in dictionary: 
		msg = 'Consultou: '+str(data[1]) + ' : ' + str(dictionary[data[1]])
		print(str(endr)+ ': Consultou '+ str(data[1])+ ' : ' + str(dictionary[data[1]]))

	#Caso a chave nao exista no dicionario
	#Guarda a mensagem de que o resultado da busca e vazio
	#loga no servidor
	else:
		#msg = 'Chave nao existe no dicionario'
		msg = 'Consultou: '+str(data[1]) + ' : ' 
		print(str(endr)+ ': tentou consultar chave nao existente '+ str(data[1]))

	#retorna amensagem a ser enviada
	return msg


#Funcao delete do admnistrado
def delete(dictionary,lock):

    #Adquirimos um lock para 
    #proteger a integridade do dicionario
    #perante varias requisicoes concorrentes
    lock.acquire()

	#Pega a chave a ser deletada
    print("Digite a chave a ser deletada")
    key = input()

    #Se ela existe, deleta do dicionario
    if key in dictionary:
        del dictionary[key]
        msg = "Chave deletada"

    #Caso contrario, so guada mensagem 
    #de que nao existe a chave para deletar
    else:
        msg = "Chave nao existe"

    #Loga se deletou ou nao
    print(msg)

    #liberamos o lock
    lock.release() 

    return


#Alteracao no atendeRequisicoes dada em aula
def atendeRequisicoes(clisock, endr, lock):

	#Variavel de bytes recebidos comecando vazio
	bytesRec = b''

	#Enquanto mantem a conexao com o cliente
	#espera receber um chunk vazio
	#que sinaliza se a conexao foi fechada pelo cliente
	while True:
		chunk = clisock.recv(1024)
		if not chunk:
			print(str(endr) + ': desconectado')
			clisock.close() 
			return

		#Enquanto o servidor estiver recebendo mensagem do cliente
		#vai guardando os chunks nos bytes recebidos
		bytesRec += chunk 

		#O servidor tenta construir os bytes recebidos em uma mensagem
		try:
			data = pickle.loads(bytesRec)

			#Trata a mensagem enviada pelo cliente
			#podendo inserir ou consultar o dicionario
			if(data[0]==1): msg = insert(clisock,endr, data, lock)

			elif(data[0]==2): msg = query(endr, data)

			else: msg = 'Se voce recebeu essa mensagem, algo deu errado'

			#Depois de inserir/consultar
			#o servidor prepara uma mensagem para retornar ao cliente
			#pegamos o tamanho da mensagem
			msgLen = len(msg)

			#Enviamos inicialmente ao cliente o tamanho da mensagem
			#para ele ficar recebendo a mensagem ate chegar ao tamanhoo correto
			clisock.sendall(msgLen.to_bytes(4, byteorder='big'))

			#Enviamos a mensagem em si
			clisock.sendall(msg.encode('utf-8'))

			#Limpamos o buffer para a proxima mensagem
			bytesRec = b''

		#Caso a mensagem nao esteja completa ainda
		#capturamos a excecao e continuamos o loop
		#para receber a mensagem completa
		except(pickle.UnpicklingError, EOFError): continue


#Funcao para carregar o dicionario
def load(dictionary):

	#Tentamos carregar o dicionario de um arquivo novo
	try: 
		with open('dictionary.pickle', 'rb') as f: 
			loadDict = pickle.load(f)
			print("Dicionario carregado")
			dictionary.update(loadDict)

	#Caso nao exista um arquivo, iniciamos o dicionario
	except FileNotFoundError: 
		dictionary = manager.dict()
		print("Dicionario novo criado")


#Funcao papra salvar o dicionario num arquivo
def save(dictionary):
	with open('dictionary.pickle', 'wb') as f: 
		pickle.dump(dict(dictionary), f)
		print("Dicionario salvo")
	return


def main():

	#ligamaos a global dicionario criada no inicio do codigo
	global dictionary 

	#Carregamos o dicionario
	load(dictionary)
	
	clientes=[]
	sock = iniciaServidor()
	lock = multiprocessing.Lock()
	print("Pronto para receber conexoes...")

	#Pequena interface para o administrador do servidor
	print("Comandos:\ncheck:  Mostra o Dicionario\ndelete: Deletar uma chave\nfim:    Finalizar apos fim de requisicoes")

	while True:
		leitura, escrita, excecao = select.select(entradas, [], [])
		for pronto in leitura:
			if pronto == sock:  
				clisock, endr = aceitaConexao(sock)
				print (str(endr) + ': conectado')
				cliente = multiprocessing.Process(target=atendeRequisicoes, args=(clisock,endr, lock))
				cliente.start()
				clientes.append(cliente) 
			elif pronto == sys.stdin: 
				cmd = input()

				#Tratar os comandos do administrador
				if cmd == 'check': print(dictionary)
				elif cmd == 'delete': delete(dictionary,lock)
				elif cmd == 'fim': 
					for c in clientes: c.join()
					sock.close()

					#Salva o dicionario no arquivo
					save(dictionary)

					sys.exit()


main()