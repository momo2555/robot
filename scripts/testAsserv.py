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
            OpenLoop().start()
            pass
        elif(data["request"]=="start_diff_speed"):
            DiffSpeed().start()
    pass
class OpenLoop(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        cons = 0
        while cons <= 1:
            left = cons
            right = cons
            consignToSend = Twist(Vector3(left, right, 0), Vector3(0, 0, 0))
            consPub.publish(consignToSend)
            time.sleep(1)
            cons+=0.1

        #arrêter le rbot
        consignToSend = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        consPub.publish(consignToSend)
class DiffSpeed(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        cons = 1
        consignToSend = Twist(Vector3(cons, cons, 0), Vector3(0, 0, 1))
        consPub.publish(consignToSend)
        time.sleep(8)
        #arret
        consignToSend = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        consPub.publish(consignToSend)


rospy.init_node("test_aserv")

consPub = rospy.Publisher('robot_consign', Twist, queue_size=10)
rospy.Subscriber("server_req", String, getreq)
rospy.spin()