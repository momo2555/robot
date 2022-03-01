#!/usr/bin/env python
import json
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from threading import Thread
from nav_msgs.msg import Odometry
import math
import time


class posAsserv(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__cons = [0, 0, 0]
        self.__pos = [0, 0, 0]
        self.__velCons = [0, 0]
        self.__precision = 0.16
        self.__k1 = 0.48
        self.__k2 = 3 
        self.__vmax = 0.3
        self.__wmax = 1
        self.__go = False
        pass
    def setPos(self, posOdom):
        x = posOdom.pose.pose.position.x
        y = posOdom.pose.pose.position.y
        sin = posOdom.pose.pose.orientation.z
        cos = posOdom.pose.pose.orientation.w
        th = math.atan2(sin, cos)*2
        self.__pos = [x, y, th]
        pass

    def setCons(self, x, y, th):
        self.__cons = [x, y, th]
        print("set postion consigne (" + str(x) + ";" + str(y) + ';' + str(th) + ')')
        
        consignToSend = Twist(Vector3(0, 0, 0), Vector3(0, 0, 3))
        consPub.publish(consignToSend)
        time.sleep(1)
        self.__go = True


    def run(self):
        print('start the thread')
        
        
        while(True):
            if(self.__go):
                dx = self.__cons[0] - self.__pos[0]
                dy = self.__cons[1] - self.__pos[1]
                if (math.sqrt(dx**2 + dy**2) > self.__precision):
                    theta = self.__pos[2]
                    delta = math.atan2(dy, dx) - theta 
                    
                

                    consv = self.__k1 * math.cos(delta) 
                    consw = self.__k2 * delta
                    print("delta=",delta,"theta=",theta,"consw=",consw)
                    #print('v = ', consv)
                    #print('w = ', consw)
                    #print('x=', self.__pos[0], ';y=', self.__pos[1])
                    if consv > self.__vmax:
                        consv = self.__vmax
                    if consv < -self.__vmax:
                        consv = -self.__vmax
               
                    if consw > self.__wmax:
                        consw = self.__wmax
                    if consw < -self.__wmax:
                        consw = -self.__wmax
                

                    consignToSend = Twist(Vector3(consv,0 , 0), Vector3(consw, 0, 2))
                    consPub.publish(consignToSend)


                    time.sleep(0.06)
                else:
                    print("fin") 
                    consignToSend = Twist(Vector3(0,0 , 0), Vector3(0, 0, 2))
                    time.sleep(1.5)
                    consignToSend = Twist(Vector3(0,0 , 0), Vector3(0, 0, 0))
                    consPub.publish(consignToSend)
                    self.__go = False
                    pass
        pass

def beginAsserv(req):
    data = json.loads(req.data)
    if(data["type"]=="request"):
        if(data["request"]=="position_cons"):
            x = float(data["x"])
            y = float(data["y"])
            th = float(data["th"])
            asserv.setCons(x, y, th)
            
            pass
    pass

rospy.init_node("pos_asserv")

consPub = rospy.Publisher('robot_consign', Twist, queue_size=10)
asserv = posAsserv()
asserv.start()
rospy.Subscriber("server_req", String, beginAsserv)
rospy.Subscriber("enc_velocity", Odometry, asserv.setPos)
rospy.spin()