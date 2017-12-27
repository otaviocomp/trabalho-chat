#Felipe Ferreira Barbosa
#Otavio do Espirito Santo
from socket import * # sockets
import threading # threadss
import time
global lUsuarios 
global lConections
global lIP
global message

lUsuarios = []
lConections = []
lIP = []


class abrirSala(threading.Thread):
	def __init__(self,serverSocket,serverPort):
		threading.Thread.__init__(self)
		self.socket = serverSocket
		self.port = serverPort
	def run(self):
		esperaConexao(self,self.socket,self.port)     
def esperaConexao(th,socket,port):
	global lUsuarios 
	global lConections
	global lIP
	connectionSocket, addr = socket.accept()	
	UserName = connectionSocket.recv(1024)
	if UserName != 'nick' and connectionSocket != 'localhost':
		lUsuarios.append(UserName+"")
		lConections.append(connectionSocket)
		lIP.append(addr)
		sentence= "Cliente " + UserName + " conectou-se"
		print sentence
		for x in lConections:
				x.send(sentence) 
		thread1 = abrirSala(socket,port)
		thread1.start()
		timer = time.time()
		count = 0
		while 1:
			sentence = connectionSocket.recv(1024)
			try:
				count= count+1
				time2 =  time.time() -timer
				if ((count == 6) and (time2<=2)):	
						connectionSocket.send("Anti-Flood: Aguarde 10 segundos...")
						time.sleep(10)
						timer=time.time()
						count =0
				if(time2>2):
					timer=time.time()
					count =0		
				if sentence == "sair()":
					lUsuarios.remove(UserName)	
					lConections.remove(connectionSocket)
					lIP.remove(addr)
					connectionSocket.close()
					th._is_running = False
					print UserName+" saiu!!"
					for x in lConections:
						x.send(UserName+" saiu!!") 
					break
				if sentence[0:5] == "nome(" and sentence[-1] == ')':
					cont = 0
					tam = len(sentence[6:]) - 1
					for x in sentence[6:]:
						if x == ' ':
							cont = cont + 1	
					if cont == tam or sentence == 'nome()':
						connectionSocket.send('nome invalido, digite um nome nao vazio')
					if cont != tam and sentence != 'nome()':	
						lUsuarios[lUsuarios.index(UserName)] = sentence[5:len(sentence)-1]
						for x in lConections:
							x.send(UserName+" agore eh "+sentence[5:len(sentence)-1])
						UserName = sentence[5:len(sentence)-1]
						continue	
				elif sentence == "lista()":
					for x in range(len(lConections)):
						connectionSocket.send("<"+lUsuarios[x]+","+lIP[x][0]+","+str(port)+">\n")
					continue	
				if sentence != '':	
					sentence = "" + UserName + " escreveu: " + (sentence) + ""
				print sentence
				for x in lConections:
					x.send(sentence) 
			except:
				th._is_running = False	
				break
			
serverName = 'localhost' 
serverPort = 8000 
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.bind((serverName,serverPort)) 
serverSocket.listen(1) 
print "Server TOP! "
thread1 = abrirSala(serverSocket,serverPort)
thread1.start()
while 1:
	message = raw_input('')
	if message == "lista()":
		for x in range(len(lConections)):
			print"<"+lUsuarios[x]+","+lIP[x][0]+","+str(serverPort)+">\n"
	elif message == "sair()":
		for x in lConections:
			x.send("sair()")
		serverName = 'localhost' 
		serverPort = 8000 
		clientSocket = socket(AF_INET,SOCK_STREAM) 
		clientSocket.connect((serverName, serverPort))
		clientSocket.send('nick')
		clientSocket.send('')					
		serverSocket.close()
		break
print 'encerrando servidor...'	


			

		


 
