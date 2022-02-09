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
        self.__params = []

    def setRequest(self, request):
        self.__request = request
        self.__type = "request"

    def setMotorrequest(self, request):
        self.__request = request
        self.__type = "motor_request"

    def toObject(self):
        result=  {
            "type" : self.__type,
            "request" : self.__request
        }
        for param in self.__params:
            result[param[0]] = param[1]
        print(result)
        return result
    def toString(self):
        return json.dumps(self.toObject())

    def addParam(self, name, value):
        self.__params.append([name, value])
class ClientSocket(Thread):
    def __init__(self):
        self.__client =socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
        self.__callbacks = []
        #initialisation du client websocket
        Thread.__init__(self)

    def run(self):
        self.__client.connect(('192.168.25.11', 32233))
        print("démarrage du client")
        while True:
            response = self.__client.recv(1024)
            #fetch callbacks
            for callback in self.__callbacks:
                callback(json.loads(response.decode('utf8')))
        
    def sendMsg(self, objMsg):
        self.__client.send(json.dumps( objMsg ).encode('utf8'))
        time.sleep(0.05)

<<<<<<< HEAD
	def run(self):
		self.__client.connect(('192.168.23.11', 32233))
		print("démarrage du client")
		while True:
			response = self.__client.recv(1024)
			#fetch callbacks
			for callback in self.__callbacks:
				callback(json.loads(response.decode('utf8')))
		
	def sendMsg(self, objMsg):
		self.__client.send(json.dumps( objMsg ).encode('utf8'))
		time.sleep(0.05)
	def onReceive(self, callback):
		self.__callbacks.append(callback)
=======
    def onReceive(self, callback):
        self.__callbacks.append(callback)
>>>>>>> af925a96cbde555ae446ba1ad208562d2373b99e
