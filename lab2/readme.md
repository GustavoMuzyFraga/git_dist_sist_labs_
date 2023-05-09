- Atividade 1

1. O estilo arquitetural escolhido foi arquitetura de camadas

2. A arquitetura de software ficou da seguinte forma:

Na camada da interface: temos uma interface simples pela qual o usuário poderá escolher inserir ou consultar o dicionário.
Na camada de processamento: temos as funções consulta e insere ao dicionário
Na camada de persistência: temos o dicionário salvo na memória, uma função de carregar/salvar o dicionário num arquivo e o dicionário salvo num arquivo

Quando o usuário escolher query, ele digitará a chave e então chamará a função de consulta Dicionário na camada de processamento, que acessa o dicionário salvo na 
memória (na camada de persistência) e checa se a chave existe. Tendo a chave no dicionário, consulta Dicionário retornará à camada de interface o resultado da consulta
ou uma mensagem dizendo que a chave não existe (no caso uma consulta com a chave vazia). 

Quando o usuário escolher insert, ele digitará a chave e seu valor, que serão enviados para a camada de processamento, para que a função insere Dicionário acesse o
dicionário na memória. Caso a chave não exista no dicionário, ela será inserida com seu valor, caso contrário não inserimos. Em seguida a função insere Dicionário retorna 
uma mensagem, de que o dado foi inserido ou de que a chave já existe no dicionário, à interface que será mostrada ao usuário.

Quando abrimos o sistema, o dicionário é carregado do arquivo para a memória e quando fechamos o sistema, salvamos o dicionário no arquivo.

![image](https://user-images.githubusercontent.com/29666473/236663502-31beedc5-465b-46f4-b8be-0f6cb3f02a9a.png)


----



- Atividade 2

1. Cliente: interface simples, query (consulta) e insert

2. Servidor: consulta dicionário, insere no dicionário, dicionário salvo na memória, save/load e arquivo onde o dicionário é salvo

3. 1. Através da interface simples, o cliente digita o comando:
   2. Insert ou 1, a chave que deseja inserir e o valor da chave
   3. Insert adiciona esses argumentos numa mensagem e envia para o servidor processar com o insere no dicionário
   4. O servidor checa se a chave no banco, caso não exista ele salva uma mensagem dizendo que adicionou, caso contrário salva uma mensagem dizendo que a chave existe
   5. Em seguida o servidor envia essa mensagem para o cliente receber pelo insert
   6. Por fim, o insert exibe a mensagem na interface simples

-

3. 1. Através da interface simples, o cliente digita o comando:
   2. Query ou 2, a chave que deseja consultar
   3. Query adiciona esses argumentos numa mensagem e envia para o servidor processar com o consulta dicionário
   4. O servidor checa se a chave no banco, caso não exista ele salva uma mensagem com consulta vazia, caso contrário salva uma mensagem com o valor
   5. Em seguida o servidor envia essa mensagem para o cliente receber pelo query
   6. Por fim, o query exibe a mensagem na interface simples



![image](https://user-images.githubusercontent.com/29666473/236663571-b66ad1d7-becb-4039-b265-9f6fed7e21ab.png)

----


- Atividade 3

Notas:

Inicialmente foi pensado em apenas 3 funcionalidades, inserir, consultar e deletar. Desde o início, ja tinha uma visão breve da arquitetura de sistemas. Especificamente, inserir e consultar, que tiveram que ser partidas entre cliente e servidor, então foram criados Insert (e inserir no dicionário) e Query (e consuta dicionário). Logo uma parte ficou para a camada de interface e a outra para processamento. E a função de deletar, como pedido no trabalho, apenas era realizada pelo administrador, então esta também ficou na camada de processamento. Depois dessa parte ter sido pensada, havia a necessidade de uma funcionalidade que salvava/carregava o dicionário no/do arquivo, então o save/load foi criado. Novamente, como apenas o servidor ficaria com o dicionário, não tinha necessidade de nenhuma parte dele ficar para o cliente.

Na parte do código, utilizei como base o código de multiprocessing dado em aula e funções como delete, save/load foram simples. Para o dicionário ser consistente entre todos os processos, eu tive que iniciar um manager. Além disso, eu utilizei um lock na função de insert e delete para preservar a integridade da estrutura de dados (dicionário).




