import rospy
import String
import json
import time
from geometry_msgs.msg import Twist, Vector3
from threading import Thread

def getreq(req):
    data = json.loads(req)
    if(data["type"]=="request"):
        if(data["request"]=="start_open_loop"):
            openLoop().start()
            pass
        
    pass
class OpenLoop(Thread):
    def __init__(self):
        thread.__init__(self):
    def run(self):
        cons = 0:
        while cons <= 1:
            left = cons
            right = cons
            consignToSend = Twist(Vector3(left, right, 0), Vector3(0, 0, 0))
            consPub.publish(consignToSend)
            time.sleep()
            cons+=0.1

        #arrêter le rbot
        consignToSend = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        consPub.publish(consignToSend)
rospy.init_node("test_aserv")

consPub = rospy.Publisher('robot_consign', Twist, queue_size=10)
rospy.Subscriber("server_req", String, getreq)
pub
rospy.spin()