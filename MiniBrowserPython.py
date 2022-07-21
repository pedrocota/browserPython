# coding utf-8
# MiniBrowser.py

import os
import sys
import socket
from urllib import parse
import tempfile
import webbrowser

# Requisitando link do servidor e porta
serverName = input("Entre com o endereço do servidor HTTP: ")
serverPort = int(input("Entre com o número da porta: "))
# Definindo tipo de socket no caso IPV4
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conectando ao socket
try:
    clientSocket.connect((serverName, serverPort))
    print("#conectando ao servior")
except:
    print("#Erro ao conectar  \n..Fechando..")
    sys.exit()

print("\n#Requisitando no servidor: ", serverName)
request = "GET / HTTP/1.1\r\nHost: " + serverName + "\r\nConnection: close \r\n\r\n"

print("#Enviando requisição")
clientSocket.sendall(request.encode('utf-8'))

# comecando a trabalhar com o arquivo que vai receber o html
f = open("index.html", "bw")  # limpando se já existir
f.close()
f = open("index.html", "br+")  # vai receber o HTML sem HTTP header

body = b""  # vai armazenar o recebido do servidor de socket

# salvando dados da request na variável body

print("#--->salvando requisição<---")
while True:
    peca = clientSocket.recv(4096)
    body = body + peca
    if len(peca) < 1:
        break

# retirando o header da variável body para escrita
headers = body.split(b'\r\n\r\n')[0]
body = body[len(headers) + 4:]

# escrevendo no arquivo
f.write(body)

# decodificando com caracteres asiaticos utf-8 nao funciona
body = body.decode('ISO-8859-1')

# output: HTML no terminal
print(body)

# passando o caminho do arquivo html salvo para ser aberto no browser
url = 'file://' + os.path.realpath('index.html')

# Renderizando o arquivo com o módulo webbrowser
webbrowser.open(url, new=1)  # abrindo o código html

f.close()
clientSocket.close()
