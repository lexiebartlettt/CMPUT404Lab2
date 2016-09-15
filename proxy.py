#!/usr/bin/env python

import socket 
import os

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.bind(("0.0.0.0",8000))
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientSocket.listen(5)


while True:
	(incomingSocket, address) = clientSocket.accept()
	print("We got a connection from %s!" % (str(address)))

	pid = os.fork()
	if (pid == 0): #We must be the child process so we will handle proxying 

		googleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		googleSocket.connect(("www.google.com",80))

		incomingSocket.setblocking(0) 
		googleSocket.setblocking(0) 

		while True: 
			skip = False
			#This half forwards from client to google
			try:
				part = incomingSocket.recv(1024)
			except socket.error, exception: 
				if exception.errno == 11: 
					skip = True
				else: 
					raise
			if not skip:
				if(len(part)>0):
					print " > "+part
					googleSocket.sendall(part) 
				else: #part will be "" when the connection is done
					exit(0)
			skip = False
			#This half forwards from google to client
			try:	
				part = googleSocket.recv(1024)
			except socket.error, exception: 
				if exception.errno == 11: 
					skip = True 
				else: 
					raise

			if not skip: 	

				if(len(part)>0):
					print " < "+part
					incomingSocket.sendall(part) 
				else: #part will be "" when the connection is done
					exit(0)


