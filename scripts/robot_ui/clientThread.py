from threading import Thread

import socket
import time
import json

class GetPositionThread(Thread):
	def __init__(self, client):
		Thread.__init__(self)
		self.__client = client
		
	
	def run(self):
		print("start position getter thread")
		while True:
			#create a new request
			rqt = serverMsg()
			rqt.setRequest("get_position")
			#send request
			self.__client.sendMsg(rqt.toObject())
			time.sleep(0.1)


class serverMsg():
	def __init__(self):
		self.__type = "request"
		self.__request = "none"
	def setRequest(self, request):
		self.__request = request
		self.__type = "request"

	def toObject(self):
		return {
			"type" : self.__type,
			"request" : self.__request
		}
	def toString(self):
		return json.dumps( self.toObject() )

class ClientSocket(Thread):
	def __init__(self):
		self.__client =socket.socket(
    				socket.AF_INET, socket.SOCK_STREAM)
		self.__callbacks = []
		#initialisation du client websocket
		Thread.__init__(self)
		
		
	

	def run(self):
		self.__client.connect(('192.168.236.11', 32233))
		print("démarrage du client")
		while True:
			response = self.__client.recv(1024)
			print(response)
			#fetch callbacks
			for callback in self.__callbacks:
				callback(json.loads(response.decode('utf8')))
		
	def sendMsg(self, objMsg):
		self.__client.send(json.dumps( objMsg ).encode('utf8'))
	def onReceive(self, callback):
		self.__callbacks.append(callback)