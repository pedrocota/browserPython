import os
import sys
import socket 
from urllib import parse 
import tempfile
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWebEngine, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QtWidgets.QMainWindow): 
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)

        self.browser = QWebEngineView()
        self.browser.setHtml(body.decode('ISO-8859-1'))  
        self.browser.setStyleSheet(body)              
        self.setCentralWidget(self.browser)
        self.show()
        self.setWindowTitle("***MINIBROWSER DALISON E PEDRO***")
  
    
app = QApplication(sys.argv)

serverName = "www.google.com"
#serverName = input("Entre com o endereço do servidor HTTP: ")
serverPort = int(input("Entre com o número da porta: "))

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort)) #conectando ao socket

#convertendo serverName para Ip
# =============================================================================
# url = parse.urlparse(serverName)
# serverIP = socket.gethostbyname(url[1])
# print ("O que é a o método:", url[0]) #https://
# print ("O que é a url:", url[1]) #www.google.com
# =============================================================================

print("\n Nome introduzido no servidor: ", serverName)

request = "GET / HTTP/1.1\r\nHost: " + serverName + "\r\nConnection: close \r\n\r\n"
clientSocket.sendall(request.encode('utf-8'))

## começando a trabalhar com dois arquivos: um vai receber o html + http header
## enquanto o outro irá receber isso sem o http reader, e será utilizado

f = open("arquivoBodyComHeader", "w") #limpando se já existir
h = open("htmlSemHeader", "w") #lwimpando se já existir
f.close() 
h.close() 

f = open("arquivoBodyComHeader", "r+") #vai receber o HTML com HTTP header
h = open("htmlSemHeader", "r+") #vai receber o HTML sem header de f

body = b"" #vai armazenar o recebido do servidor de socket

#salvando request em body

while True:
    peca = clientSocket.recv(4096)
    body = body + peca;
    if len(peca) < 1:     
        break

headers =  body.split(b'\r\n\r\n')[0]
body = body[len(headers)+4:]

str_name = "<!doctype html>" #definindo o fim do HTTP header

# =============================================================================
# f.write(body) #salvando body em f
# f.close() #f agora será utilizado apenas para leitura, abaixo
# f = open("arquivoBodyComHeader", "r") 
# 
# 
# lines = f.readlines()
# for line in lines:
#     if str_name in line:
#         start = lines.index(line)
#         lines = lines[start::1]
#         break
# 
# for line in lines:
#     h.write(f"{line}")
# 
# print(h.read())
# h.close()
# 
# h = open ("htmlSemHeader", "r")
# body = h.read() #body agora vai ser só HTML
# 
# print ("O que passou por body é:", body)
#  
# =============================================================================
window = MainWindow()
app.exec_()
f.close()
h.close()
clientSocket.close()
