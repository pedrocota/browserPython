import os
import sys
import socket 
from urllib import parse 
import tempfile
import webbrowser

#serverName = "www.google.com"
serverName = input("Entre com o endereço do servidor HTTP: ")
serverPort = int(input("Entre com o número da porta: "))
#serverPort = 80
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort)) #conectando ao socket

print("\n Nome introduzido no servidor: ", serverName)

request = "GET / HTTP/1.1\r\nHost: " + serverName + "\r\nConnection: close \r\n\r\n"
clientSocket.sendall(request.encode('utf-8'))

#comecando a trabalhar com o arquivo que vai receber o html
f = open("index.html", "bw") #limpando se já existir
f.close() 
f = open("index.html", "br+") #vai receber o HTML sem HTTP header

body = b"" #vai armazenar o recebido do servidor de socket


#salvando dados da request na variável body

while True:
    peca = clientSocket.recv(4096)
    body = body + peca;
    if len(peca) < 1:     
        break

#retirando o header da variável body para escrita
headers =  body.split(b'\r\n\r\n')[0]
body = body[len(headers)+4:]

#escrevendo no arquivo
f.write(body)

#output: HTML
print(body)

body = body.decode('ISO-8859-1')
url = 'file://' + os.path.realpath('index.html')

webbrowser.open(url,new=1) #abrindo o código html

f.close()
clientSocket.close()
