from getpass import getpass
from socket import *
import threading 
import time
global message
global sentence
message = ''
class envMsg(threading.Thread):
	def __init__(self,serverName,serverPort,clientSocket):
		threading.Thread.__init__(self)
		self.sn = serverName
		self.sp = serverPort
		self.cs = clientSocket
	def run(self):
			env(self,self.sn,self.sp,self.cs)
def env(th,serverName,serverPort,clientSocket):
	global message
	global sentence
	while 1:
		try:
			if message == "Anti-Flood: Aguarde 10 segundos...":
				message=''
				time.sleep(10)
			if sentence != 'sair()':	
				message = raw_input()
				clientSocket.sendto(message,(serverName, serverPort))
			if message == "sair()" or sentence == 'sair()':
				clientSocket.close() 
				th._is_running = False
				break	
		except:
			clientSocket.close() 
			th._is_running = False		
			break
	
serverName = 'localhost' 
serverPort = 8000 
clientSocket = socket(AF_INET,SOCK_STREAM) 
clientSocket.connect((serverName, serverPort)) 
while 1:
	cont = 0
	sentence = raw_input('Usuario: ')
	tam = len(sentence)
	for x in sentence:
		if x == ' ':
			cont = cont + 1
	if cont == tam:
		print 'nome invalido, digite um nome nao vazio'				
	if cont != tam:
		break
clientSocket.send(sentence)
print("Bem vindo ao Servidor Top \nPara conversar, basta digitar \nMas preste bastante atencao \n Para sair, digite sair() \n Para mudar seu Nickname, digite name(NovoNome) \n Para ver os participantes da sala, digite lista() \n chat: \n")
reciveSentence = clientSocket.recv(1024)
print '\r'+reciveSentence+''
msg = envMsg(serverName,serverPort,clientSocket)
msg.start()
while 1:
	if(message == "sair()"):
		print "Saindo em 3..."
		time.sleep(1)
		print "Saindo em 2..."
		time.sleep(1)
		print "Saindo em 1..."
		time.sleep(1)
		print "Tchau tchau"
		break
	if(sentence != 'sair()'):	
		sentence = clientSocket.recv(1024)
	elif(sentence == 'sair()'):
		print 'Ops, o servidor caiu! Pressione a tecla "Enter" para sair.'
		clientSocket.close()
		break
	print sentence
	if(sentence == "Anti-Flood: Aguarde 10 segundos..."):
		message=sentence
		time.sleep(10)	
