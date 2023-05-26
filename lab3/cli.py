
# Cliente de echo usando RPC
import rpyc #modulo que oferece suporte a abstracao de RPC

# endereco do servidor de echo
SERVIDOR = 'localhost'
PORTA = 10001

def iniciaConexao():
	conn = rpyc.connect(SERVIDOR, PORTA) 
	return conn

def fazRequisicoes(conn):

	while True: 

		tosend =[]
		msg = input("0 ou fim - encerrar\n1 ou insert - insere no dicionario\n2 ou query - consulta no dicionario\n3 ou del - deleta chave dicionario\n4 ou save - salva o dicionario\n")
		if msg == 'fim' or msg == '0': break


		#Insert para inserir no dicionario
		elif msg == 'insert' or msg == '1':
			tosend.append(1)
			print("Diga a chave do dicionario: ")
			tosend.append(input())
			print("Diga o valor da chave: ")
			tosend.append(input())
			ret = conn.root.insert(tosend)

		#Query para consultar dicionario
		elif msg == 'query' or msg == '2':
			tosend.append(2)
			print("Diga a chave do dicionario: ")
			tosend.append(input())
			ret = conn.root.query(tosend)


		elif msg == 'del' or msg == '3':
			tosend.append(3)
			print("Diga a chave do dicionario a ser deletada: ")
			tosend.append(input())
			ret = conn.root.delete(tosend)


		elif msg == 'save' or msg == '4':
			print("Digite a senha para salvar o dicionario")
			ret = conn.root.save(input())

		#Else para caso alguma outra coisa seja digitada
		else:
			print("Comando desconhecido")
			continue


		# imprime a mensagem recebida
		print(ret)


	# encerra a conexao
	conn.close()

def main():
	'''Funcao principal do cliente'''
	#inicia o cliente
	conn = iniciaConexao()
	#interage com o servidor ate encerrar
	fazRequisicoes(conn)

# executa o cliente
if __name__ == "__main__":
	main()