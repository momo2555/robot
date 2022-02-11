#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import json
import time
from geometry_msgs.msg import Twist, Vector3
from threading import Thread

def getreq(req):
    data = json.loads(req.data)
    if(data["type"]=="request"):
        if(data["request"]=="start_open_loop"):
            stepDuration = float(data["duration"])
            nbStage = float(data["nb_stage"])
            consMax = float(data["cons_max"])
            RampeOpenLoop(stepDuration, nbStage, consMax).start()
            pass
        elif(data["request"]=="start_diff_speed"):
            duration = float(data["duration"])
            cons = float(data["v"])
            DiffSpeed(duration, cons).start()
        elif(data["request"]=="start_vel_speed"):
            duration = float(data["duration"])
            v = float(data["v"])
            w = float(data["w"])
            
            VelSpeed(duration, v, w).start()    
    pass
class RampeOpenLoop(Thread):
    def __init__(self, stepDuration, nbStage, consMax):
        Thread.__init__(self)
        self.__stepDuration = stepDuration
        self.__nbStage = nbStage
        self.__consMax = consMax
    def run(self):
        variation = self.__consMax / self.__nbStage
        delay = self.__stepDuration / self.__nbStage
        cons = variation
        while cons <= self.__consMax:
            left = cons
            right = cons
            consignToSend = Twist(Vector3(left, right, 0), Vector3(0, 0, 0))
            consPub.publish(consignToSend)
            time.sleep(delay)
            cons+=variation
        while cons > 0:
            left = cons
            right = cons
            consignToSend = Twist(Vector3(left, right, 0), Vector3(0, 0, 0))
            consPub.publish(consignToSend)
            time.sleep(delay)
            cons-=variation
        #arrêter le rbot
        consignToSend = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        consPub.publish(consignToSend)

class DiffSpeed(Thread):
    def __init__(self, duration, cons):
        Thread.__init__(self)
        self.__duration = duration
        self.cons = cons
    def run(self):
        cons = self.cons
        consignToSend = Twist(Vector3(cons, cons, 0), Vector3(0, 0, 1))
        consPub.publish(consignToSend)
        time.sleep(self.__duration)
        #arret
        consignToSend = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        consPub.publish(consignToSend)
class VelSpeed(Thread):
    def __init__(self, duration, v, w):
        Thread.__init__(self)
        self.__duration = duration
        self.__v = v
        self.__w = w
    def run(self):
        v = self.__v
        w = self.__w
        consignToSend = Twist(Vector3(v, 0, 0), Vector3(w, 0, 2))
        consPub.publish(consignToSend)
        time.sleep(self.__duration)
        #arret
        consignToSend = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        consPub.publish(consignToSend)


rospy.init_node("test_aserv")

consPub = rospy.Publisher('robot_consign', Twist, queue_size=10)
rospy.Subscriber("server_req", String, getreq)
rospy.spin()