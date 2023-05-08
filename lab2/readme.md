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






- Atividade 2

1. Cliente:

2. Servidor:

3. 

![image](https://user-images.githubusercontent.com/29666473/236663571-b66ad1d7-becb-4039-b265-9f6fed7e21ab.png)
