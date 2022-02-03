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
            stepDuration = float(data["stage_time"])
            RampeOpenLoop(stepDuration).start()
            pass
        elif(data["request"]=="start_diff_speed"):
            duration = float(data["duration"])
            cons = float(data["v"])
            DiffSpeed(duration, cons).start()
    pass
class RampeOpenLoop(Thread):
    def __init__(self, stepDuration):
        Thread.__init__(self)
        self.__stepDuration = stepDuration
    def run(self):
        cons = 0
        while cons <= 1:
            left = cons
            right = cons
            consignToSend = Twist(Vector3(left, right, 0), Vector3(0, 0, 0))
            consPub.publish(consignToSend)
            time.sleep(self.__stepDuration)
            cons+=0.1

        #arrêter le rbot
        consignToSend = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        consPub.publish(consignToSend)
class OpenLoop(Thread):
    def __init__(self, stepDuration):
        Thread.__init__(self)
        self.__duration = duration
    def run(self):
        cons = 0
        while cons <= 1:
            left = cons
            right = cons
            consignToSend = Twist(Vector3(left, right, 0), Vector3(0, 0, 0))
            consPub.publish(consignToSend)
            time.sleep(self.__stepDuration)
            cons+=0.1

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


rospy.init_node("test_aserv")

consPub = rospy.Publisher('robot_consign', Twist, queue_size=10)
rospy.Subscriber("server_req", String, getreq)
rospy.spin()