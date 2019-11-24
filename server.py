#!/usr/bin/env python3
"""Server"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_conexoes():
    """Esse loop aguarda eternamente(infinito) requerimentos de possíveis clientes"""
    while True:
        """Primeiramente o objeto socket deve aceitar um determinado requerimento"""
        client, client_address = SERVER.accept()
        # O mẽtodo accept devolve um objeto socket que é a conexao
        # e o endereco do cliente que está fazendo a conexao
        enderecos[client] = client_address  # armazena o endereço do cliente no dicionário de endereços
        Thread(target=trata_client, args=(client,)).start()


def trata_client(client):  # Recebe o socket do cliente como argumento
    """Lida com uma única conexão de cliente."""
    """Recebendo o nome que meu cliente pretende usar para a conexão através do socket 'client' que foi 
    retornado pelo accept----- # a name terá max 1024 bytes de informacao"""
    name = client.recv(1024).decode("utf8")
    client.send(bytes(name + " está online!", "utf8"))
    msg = "%s entrou no chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name  # armazena o nome do cliente no dicionário de nomes(clients)

    while True:
        # loop infinito de comunicacao
        msg = client.recv(1024)  # recebendo uma mensagem do cliente
        """se uma mensagem não contém instruções para sair, simplesmente transmitimos 
        a mensagem para outros clientes conectados"""
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + "")
        else:   # mensagem com instrucao de saída
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s saiu do chat" % name, "utf8"))
            break


"""Se encontrarmos uma mensagem com instruções de saída (ou seja, o cliente envia uma {sair}), 
repetimos a mesma mensagem para o cliente(ela aciona uma ação de fechamento no lado do cliente)
e fechamos o soquete de conexão para ele"""


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Envia a mensagem para todos os cliente conectados."""
    """Passamos um prefixo para broadcast () em nossa função trata_client(),
    fazemos isso para que as pessoas possam ver exatamente quem é o remetente de uma mensagem específica"""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


" Definindo as constantes "
clients = {}    # Dicionário responsável por armazenar os clientes
enderecos = {}  # Dicionário responsável por armazenar os enderecos

"""Criando o nome do Host (aquele que vai receber os pedidos do cliente)"""
HOST = "localhost"

"""Definindo número de porta"""
PORT = 50000

ADDR = (HOST, PORT)     # Constante que armazena meu endereco e número de porta

"""
Criando um objeto socket:
Em que a primeira constante (AF_INET) representa a família do endereco, 
já a segunda constante representa um SOCKET STREAM ou um DATAGRAM (socket.SOCK_DGRAM),
um terceiro valor opcional pode ser passado como atributo do objeto SOCKET, o protocolo, no qual
o padrão é 0.
O atributo AF_INET indica que é um protocolo de endereco de  IP
O atributo SOCKET_STREAM que foi passado, indica que é um protocolo de transferencia TCP
A combinacão dos dois atributos indica que está sendo criado um servidor do tipo TCP/IP
"""
SERVER = socket(AF_INET, SOCK_STREAM)

"""Após criado o servidor por meio de um socket, o objeto deve ser vinculado a um 
endereco e numero de porta"""
SERVER.bind(ADDR)

"""Iniciando o servidor e aceitando requisicoes"""
if __name__ == "__main__":
    SERVER.listen(5)
    print("Aguardando conexão...")
    ACCEPT_THREAD = Thread(target=accept_conexoes)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()
