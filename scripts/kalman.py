#!/usr/bin/env python
import rospy
import time
import json
from threading import Thread
from robot.srv import encoders, encodersResponse
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import tf
import sys
import math
from tf.transformations import quaternion_from_euler

#lecture fichier de config


class kalmanProcess():
    def __init__(self):
        
        self.__d = 274.4
        self.__r = 32
        self.__tpr = 1000
        self.__lastTime = 0
        self.__currentTime = 0
        self.__encTicks = [0, 0] #(left, right)
        self.__lastEncTicks = [-1, -1] 
        self.__encDiffSpeed = [0, 0] #(vleft, vright)
        self.__localVelocity = [0, 0] #(vx, w)
        self.__velocity = [0, 0, 0] #(vx,vy, omega)
        self.__position = [0, 0, 0]
        self.__maxTicks = 65535
        self.__maxSafeTicks = 500
            
    def start(self):
        
        self.__lastTime = rospy.Time.now()
        dt = 0
        while(True):
            
            #get the the encoders data
            time.sleep(0.01)
            #print(self.__encTicks)
            #self.__lastTime = rospy.Time.now()
            #récupération des données des encodeurs
            data = encoders_client()
            #on enregistre les anciennes valeurs des encodeurs
            self.__lastEncTicks = self.__encTicks
            #enregistre les données récupérées
            self.__encTicks = [data[0], data[1]]
            #temps actuel
            self.__currentTime = rospy.Time.now()
            #calcul de dt
            dt =  (self.__currentTime- self.__lastTime).to_sec()
            #sauvegarde du temps dans une autre variable
            self.__lastTime = self.__currentTime
            if(self.__encTicks[0] != -1 and self.__encTicks != -1):
                if dt > 0:
                    #calcul des vitesses et de la position
                    self.FigureSpeed(dt)
                    #envoie des données pour la position estimée
                    velocityPublisher(self.__position[0], self.__position[1], self.__position[2], 
                                        self.__localVelocity[0], self.__localVelocity[1],
                                        self.__currentTime, self.__encDiffSpeed[0], self.__encDiffSpeed[1])
                    pass
                #print("dt={0:.2f}; th={1:.2f}; x={2:.2f}; y={3:.2f}".format(dt, self.__position[2], self.__position[0], self.__position[1]))
                
              
    def FigureSpeed(self, dt):
        #si 
        if self.__lastEncTicks == [-1, -1]:
            self.__lastEncTicks = self.__encTicks
        dright = self.__encTicks[1] - self.__lastEncTicks[1]
        dleft = self.__encTicks[0] - self.__lastEncTicks[0]
        if(abs(dright) > self.__maxSafeTicks):
            dright = ((-1, 1)[dright>=0])*(self.__maxTicks>>2) -  dright
            
        if(abs(dleft) > self.__maxSafeTicks):
            print(self.__encTicks[0], ';', self.__lastEncTicks[0])
            dleft = ((-1, 1)[dleft>=0])*(self.__maxTicks>>2) -  dleft
           
        #left wheel
        leftSpeed = (dleft)/self.__tpr
        leftSpeed = leftSpeed * self.__r * 2 * math.pi / 1000 #conversion en metre
        leftSpeed = leftSpeed/dt

        rightSpeed = (dright)/self.__tpr
        rightSpeed = rightSpeed * self.__r * 2 * math.pi / 1000 #conversion en metre
        rightSpeed = rightSpeed/dt    

        self.__encDiffSpeed = [leftSpeed, rightSpeed] 
        """rightSpeed=self.__encTicks[1]
        leftSpeed=self.__encTicks[0]
        self.__encDiffSpeed = [self.__encTicks[0], self.__encTicks[1]]"""
        w = (rightSpeed - leftSpeed)/self.__d*1000
        v = (rightSpeed + leftSpeed)/2
        self.__localVelocity = [v, w]
        vx = v*math.cos(self.__position[2])
        vy = v*math.sin(self.__position[2])
        self.__velocity=[vx,vy , w]

        dx = vx*dt
        dy = vy*dt
        dth = w*dt

        self.__position[0]+=dx
        self.__position[1]+=dy












        
        self.__position[2] = self.reduceAngle(self.__position[2] + dth)


        pass
    def reduceAngle(self, x): 
        a = math.fmod(x, 2*math.pi)
        return a
        
def velocityPublisher(x, y, th, v, w, t, vl, vr):
    if not rospy.is_shutdown():
        odomQuat = quaternion_from_euler(0, 0, th)
        """odomBroadcaster.sendTransform(
            (x, y, 0),
            odomQuat,
            t,
            "base_link",
            "odom"
        )"""
        message = Odometry()
        message.header.stamp = t
        message.header.frame_id = "odom"
        message.pose.pose = Pose(Point(x, y, 0), Quaternion(*odomQuat))
        
        message.child_frame_id = "base_link"
        message.twist.twist = Twist(Vector3(v, 0, 0), Vector3(0, 0, w))
        #print(message)

        odomPub.publish(message)

        diffMsg = Twist(Vector3(vl, vr, 0), Vector3(0, 0, 0))
        diffVelPub.publish(diffMsg)
    pass

def encoders_client():
    rospy.wait_for_service('encoders')
    get_encoders = rospy.ServiceProxy('encoders', encoders)
    cmd = 1
    rep = get_encoders(cmd)
    return (rep.left, rep.right)

if __name__ == "__main__":
    #initialisation du noeud
    rospy.init_node("kalman", anonymous=False)
    odomPub = rospy.Publisher("enc_velocity", Odometry, queue_size=10)
    diffVelPub = rospy.Publisher("diff_velocity", Twist, queue_size=10)
    #initialtisation du tf
    odomBroadcaster = tf.TransformBroadcaster()
    #filtre de kalman
    kalman = kalmanProcess()
    print("start kalman process")
    kalman.start()
    """print("\quit to exit")
    while 1:
        strIn = input("cmd: ")
        if strIn == "\quit":
            sys.exit()"""

    
    
