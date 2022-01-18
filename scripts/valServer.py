#!/usr/bin/env python
import rospy
import asyncio
import websockets
import math
import json
from nav_msgs.msg import Odometry
import socket
from threading import Thread


class ServerSocket(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(("localhost", 32233))
        self.__server.listen(1)
        self.__clients = []
        
    def run(self):
        print("démarrage du serveur")
        while(True):
            client, clientAddress = self.__server.accept()
            self.__clients.append(ClientProcess(client))
            self.__clients[-1].start()       

class ClientProcess(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.__client = client
    def run(self):
        print("nouveau client connecté")
        while True:
            response = self.__client.recv(1024)
            print(response)
            self.__client.send(b"ok")
print(socket.gethostname())
server = ServerSocket()
server.start()

