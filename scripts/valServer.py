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
        self.__server.bind(("192.168.236.11", 32233))
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
            self.processRequest(response)
            
    def processRequest(self, msg):
        data = json.loads(msg.decode('utf8'))
        if data["type"] == "request":
            if data["request"] == "get_position":
                #send the response
                
                response = {
                    "type" : "position",
                    "position" : robot.getPosition()
                }
                
                self.send(response)
    def send(self, objMsg):
        self.__client.send( json.dumps(objMsg).encode('utf8') )
class RosNode(Thread):
    def __init__(self):
        Thread.__init__(self)
        rospy.init_node("val_server")
    def run(self):
        rospy.Subscriber("enc_velocity", Odometry, robot.setPosition)
        rospy.spin()
    
class RobotCom():
    def __init__(self):
        self.__position = {
            "x" : 0,
            "y" : 0,
            "z" : 0
        }
    def setPosition(self, posOdom):
        self.__position["x"] = posOdom.pose.pose.position.x
        self.__position["y"] = posOdom.pose.pose.position.y
        cos = posOdom.pose.pose.orientation.w
        sin = posOdom.pose.pose.orientation.z
        self.__position["th"] = math.atan2(sin, cos)
    def getPosition(self):
        return self.__position
print(socket.gethostname())
#start server
server = ServerSocket()
server.start()
#communication interrobot
robot = RobotCom()
#start rosnode and subscriber
rosnode = RosNode()
rosnode.start()