#!/usr/bin/env python
import json
import serial
import rospy
from robot.srv import encoders, encodersResponse
from threading import Thread
from geometry_msgs.msg import Twist, Vector3
import sys
import time

    

#position thread
class getPosThread(Thread):
    def __init__(self, serial):
        Thread.__init__(self)
        self.__serial = serial
        return
    def run(self):
        
        rospy.Service('encoders', encoders, self.handle_encoders)
        rospy.spin()

    def getPosition(self):
        sr ="enc=(-1;-1)"
        if (not self.__serial.busy()):
            self.__serial.setBusy() #---------
            print("encodeurs: envoie => ")
            getit = True
            #envoie de la commande
            self.__serial.write(b"M404 \n")
            
            #reccuperation de la valeur des encodeurs
            i = 0
            while getit:
            
                    by = self.__serial.readline()
                    sr=by.decode('utf-8')
                    getit = not "enc="in sr
                    i+=1
                    if i >2:
                        getit = False
                        sr = "enc=(-1;-1)"
            print("encodeurs: fin <= ")
            self.__serial.setUnbusy()#---------
                    
        return sr

    def handle_encoders(self, req):
        #on renvoie le position du client
        strData = self.getPosition()
        data = strData.replace('enc=(', '').replace(')', '').split(';')
        return encodersResponse(int(data[0]),int(data[1]))  


class setPosConsignThread(Thread):
    def __init__(self, serial):
        Thread.__init__(self)
        self.__serial = serial

    def run(self):
        rospy.Subscriber("robot_consign", Twist, self.getConsign)
        rospy.spin()

    def getConsign(self, cons):
        print(cons)
        sended = False
        time.sleep(0.01)
        while not sended:
            print(self.__serial.busy())
            if (not self.__serial.busy()):
                self.__serial.setBusy() #---------
                time.sleep(0.02)
                print("moteurs: envoie => ")
                gcode = "G26 X{0:.2f} Y{1:.2f} \n".format(cons.linear.x, cons.linear.y)
                print(gcode)
                x = cons.linear.x
                y = cons.linear.y
                self.__serial.write(gcode.encode("utf8"))
                sended = True
                print("moteurs: fin <= ")
                self.__serial.setUnbusy()#---------
            time.sleep(0.01)
        print("outwhile")

        pass 

class MotSerial(serial.Serial):
    def __init__(self, serialName):
        serial.Serial.__init__(self, serialName, 115200, timeout=0)
        self.__serialBusy = False
    def busy(self):
        return self.__serialBusy
    def setUnbusy(self):
        self.__serialBusy = False
    def setBusy(self):
        self.__serialBusy = True

class Verif(Thread):
    def __init__(self, ser):
        Thread.__init__(self)
        self.__serial = ser
    def run(self):
        pass
   
serialName = rospy.get_param("motor_controller_port", "/dev/ttyACM0")

print(serial.__file__)
ser = MotSerial(serialName)

#execution server position
rospy.init_node('serialCon')

posServer = getPosThread(ser)
posServer.start()

consServer = setPosConsignThread(ser)
consServer.start()

verif = Verif(ser)
verif.start()
"""print("'out' to exit")
while 1:
    strIn = input('cmd: ')
    #print(strIn)"""

