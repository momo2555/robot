#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist, Vector3

rospy.init_node('consign')
consignPublisher = rospy.Publisher('robot_consign', Twist, queue_size=10)
while True:
    commande = input("robot consign: ")
    cons = commande.split(';')
    left = float(cons[0])
    right = float(cons[1])
    print('left', left)
    print('right', right)
    consignToSend = Twist(Vector3(left, right, 0), Vector3(0, 0, 0))
    consignPublisher.publish(consignToSend)
    pass

