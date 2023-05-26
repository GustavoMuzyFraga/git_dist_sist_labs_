
# Servidor de echo usando RPC 
import rpyc #modulo que oferece suporte a abstracao de RPC
import multiprocessing
import pickle



#servidor que dispara um processo filho a cada conexao
from rpyc.utils.server import ForkingServer 


#iniciar o manager
manager = multiprocessing.Manager()
#Usamos o manager para controlar
#o dicionario entre varios processos
dictionary = manager.dict()

# porta de escuta do servidor de echo
PORTA = 10001



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
def save():
	with open('dictionary.pickle', 'wb') as f: 
		pickle.dump(dict(dictionary), f)
		print("Dicionario salvo")
	return





# classe que implementa o servico de echo
class Echo(rpyc.Service):

	def __init__(self):
		self.client_addresses = {}
		self.current_client_address = None
		self.lock = multiprocessing.Lock()

	# executa quando uma conexao eh criada
	def on_connect(self, conn):
		client_address = conn._channel.stream.sock.getpeername()
		self.client_addresses[conn] = client_address
		self.current_client_address = client_address
		print("Conexao iniciada:  ", client_address[0] + ":" + str(client_address[1]))

	# executa quando uma conexao eh fechada
	def on_disconnect(self, conn):
		client_address = self.client_addresses.pop(conn, None)
		if client_address is not None:
			print("Conexao finalizada:", client_address[0] + ":" + str(client_address[1]))


	def exposed_insert(self, data):
		#Adquirimos um lock para 
		#proteger a integridade do dicionario
		#perante varias requisicoes concorrentes
		with self.lock:

			#Se a chave ja existe no dicionario,
			#logamos no servidor a tentativa
			#e guardamos a mensagem para enviar ao cliente
			if data[1] in dictionary:    
				print(str(self.current_client_address[0]) +':'+ str(self.current_client_address[1])+ ': Tentou inserir chave existente '+ str(data[1]))
				msg = "Chave ja existe: "+str(data[1])  + ' : ' + str(dictionary[data[1]])+", valor nao inserido"

		    #Se a chave nao existe no dicionario,
		    #inserimos ela
		    #e guardamos a mensagem de adicionado para enviar ao cliente
			else:
				dictionary[data[1]]=data[2]
				print(str(self.current_client_address[0]) +':'+ str(self.current_client_address[1])+ ': Inseriu nova chave '+ str(data[1])+ ' como o valor ' + str(data[2]))
				msg = "Adicionado: " +   str(data[1])  + ' : ' + str(dictionary[data[1]])

		#retorna a mensagem a ser enviada
		return msg


	def exposed_query(self, data):
		#Se a chave consultada estiver no dicionario
		#guarda o resultado para enviar
		#loga uma mensagem no servidor
		if data[1] in dictionary: 
			msg = 'Consultou: '+str(data[1]) + ' : ' + str(dictionary[data[1]])
			print(str(self.current_client_address[0]) +':'+ str(self.current_client_address[1])+ ': Consultou '+ str(data[1])+ ' : ' + str(dictionary[data[1]]))

		#Caso a chave nao exista no dicionario
		#Guarda a mensagem de que o resultado da busca e vazio
		#loga no servidor
		else:
			#msg = 'Chave nao existe no dicionario'
			msg = 'Consultou: '+str(data[1]) + ' : ' 
			print(str(self.current_client_address[0]) +':'+ str(self.current_client_address[1])+ ': tentou consultar chave nao existente '+ str(data[1]))

		#retorna amensagem a ser enviada
		return msg

	def exposed_delete(self, data):

	    #Adquirimos um lock para 
	    #proteger a integridade do dicionario
	    #perante varias requisicoes concorrentes
		with self.lock:


		    #Se ela existe, deleta do dicionario
			if data[1] in dictionary:
				msg = "Chave deletada: "+str(data[1])+' : '+str(dictionary[data[1]])
				del dictionary[data[1]]

		    #Caso contrario, so guada mensagem 
		    #de que nao existe a chave para deletar
			else:
				msg = "Chave: "+str(data[1])+' nao possui valor'

	   
		return msg
  

	def exposed_save(self, password):

		if(password=='queroMeFormar'): 
			with self.lock:
				save()

			msg=dictionary

		else:
			msg='Senha Negada'

		return msg



# dispara o servidor
def main():

	#ligamaos a global dicionario criada no inicio do codigo
	global dictionary 

	#Carregamos o dicionario
	load(dictionary)

	srv = ForkingServer(Echo, port = PORTA)
	srv.start()


main()