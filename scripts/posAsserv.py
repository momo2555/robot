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
        self.__precision = 0.01
        self.__k1 = 1
        self.__k2 = 1
        self.__vmax = 0.5
        self.__wmax = 0.01
        pass
    def setPos(self, posOdom):
        x = posOdom.pose.pose.position.x * 1000
        y = posOdom.pose.pose.position.y * 1000
        sin = posOdom.pose.pose.orientation.w
        cos = posOdom.pose.pose.orientation.z
        th = math.atan2(sin, cos)*2
        self.__pos = [x, y, th]
        pass

    def setCons(self, x, y, th):
        self.__cons = [x, y, th]
        print("set postion consigne (" + str(x) + ";" + str(y) + ';' + str(th) + ')')


    def run(self):
        print('start')
        while(True):
            dx = self.__cons[0] - self.__pos[0]
            dy = self.__cons[1] - self.__pos[1]
            if (math.sqrt(dx**2 + dy**2) > self.__precision):
                theta = self.__pos[2]
                delta = math.atan2(dy, dx) - theta

                consv = self.__k1 * math.cos(theta)
                if consv > self.__vmax:
                    consv = self.__vmax
                if consv < -self.__vmax:
                    consv = -self.__vmax
                consw = self.__k2 * theta
                if consw > self.__wmax:
                    consw = self.__wmax
                if consw < -self.__wmax:
                    consw = -self.__wmax

                consignToSend = Twist(Vector3(consv,0 , 0), Vector3(consw, 0, 2))
                consPub.publish(consignToSend)


                time.sleep(0.1)
            else:
                print("fin")
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
            asserv.start()
            pass
    pass
asserv = posAsserv()
rospy.init_node("pos_asserv")

consPub = rospy.Publisher('robot_consign', Twist, queue_size=10)
rospy.Subscriber("server_req", String, beginAsserv)
rospy.Subscriber("enc_velocity", Odometry, asserv.setPos)
rospy.spin()