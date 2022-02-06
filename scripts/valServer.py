#!/usr/bin/env python
import rospy
import asyncio
import websockets
import math
from std_msgs.msg import String
import json
from nav_msgs.msg import Odometry
import socket
from geometry_msgs.msg import Twist, Vector3
from threading import Thread


class ServerSocket(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(("192.168.25.11", 32233))
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
            
            self.processRequest(response)
            
    def processRequest(self, msg):
        try:
            data = json.loads(msg.decode('utf8'))
            #si on reçoit une requêtte (un oprocess à éxecuter sur le robot)
            if data["type"] == "request":
                if data["request"] == "get_position":
                    #send the response
                    
                    response = {
                        "type" : "position",
                        "position" : robot.getPosition(),
                        "diffSpeed" : robot.getVelocity(),
                        "cons" : robot.getCons()
                    }
                    
                    self.send(response)
                elif data["request"] == "start_open_loop":
                    print(msg)
                    robotCons.publish(msg.decode('utf8'))
                elif data["request"] == "start_diff_speed":
                    robotCons.publish(msg.decode('utf8'))
            #si on reçoit une rerquêtte moteur (des changement à faire sur la carte moteur)
            elif data["type"] == "motor_request":
                
                robotCons.publish(msg.decode('utf8'))
                pass
        except Exception:
            pass
    def send(self, objMsg):
        self.__client.send( json.dumps(objMsg).encode('utf8') )
        
class RosNode(Thread):
    def __init__(self):

        Thread.__init__(self)
        rospy.init_node("val_server")
    def run(self):
        print("Initialisation des subscribers")
        rospy.Subscriber("enc_velocity", Odometry, robot.setPosition)
        rospy.Subscriber("robot_consign", Twist, robot.setCons)
        rospy.Subscriber("diff_velocity", Twist, robot.setVelocity)
        rospy.spin()
    
class RobotCom():
    def __init__(self):
        self.__position = {
            "x" : 0,
            "y" : 0,
            "z" : 0
        }
        self.__DiffVelocity = {
            "left" : 0,
            "right" : 0
        }
        self.__cons = {
            "left" : 0,
            "right" : 0
        }
        

    def setPosition(self, posOdom):
        #print(posOdom)
        self.__position["x"] = posOdom.pose.pose.position.x
        self.__position["y"] = posOdom.pose.pose.position.y
        sin = posOdom.pose.pose.orientation.w
        cos = posOdom.pose.pose.orientation.z
        self.__position["th"] = math.atan2(sin, cos)*2

    def setVelocity(self, diffVel):
        self.__DiffVelocity["left"] = diffVel.linear.x
        self.__DiffVelocity["right"] = diffVel.linear.y


    def getVelocity(self):
        return self.__DiffVelocity

    def getPosition(self):
        return self.__position
    def getCons(self):
        return self.__cons
    def setCons(self, cons):
        self.__cons["left"] = cons.linear.x
        self.__cons["right"] = cons.linear.y

print(socket.gethostname())
#start server
server = ServerSocket()
server.start()
#communication interrobot
robot = RobotCom()
#start rosnode and subscriber
rosnode = RosNode()
rosnode.start()
#ros publishers
robotCons = rospy.Publisher('server_req', String, queue_size=10)
#motorReq = rospy.Publisher('motor_request', String, queue_size=10)
