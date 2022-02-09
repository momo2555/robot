#!/USI/usr/bin/env python3
#!/usr/bin/env python
# license removed for brevity

from re import search
import tf
import numpy as np 
import time 
import serial
import rospy
# test 
from std_msgs.msg import String 
from sensor_msgs.msg import PointCloud, ChannelFloat32
from geometry_msgs.msg import Point32
from tf2_ros.buffer_interface import Stamped
import yaml

#-------------------------------------------------------------------------------

class Sonar():

    def __init__(self):
        self.serial = serial.Serial(port='/dev/ttyUSB0',baudrate = 115200);
        self.stream=open("/home/loic/catkin_ws/src/sonar/config/sonar_config.yaml",'r'); #TODO : Change path
        self.data=yaml.load(self.stream);
        self.sonarPos=self.data.items();

        self.publisher = rospy.Publisher('sonartopic', PointCloud, queue_size=10)
        self.odom_tf=tf.TransformBroadcaster()

    def initPos(self):
        for key,value in self.sonarPos:
            if (key=="sonars"):
                self.sonarPos=value;

    def initRos(self):
        rospy.init_node('talker', anonymous=True);

    def transform(d,x,y,th) :
        X=np.array(
            [[d/1000],
            [0],[0]])
        B=np.array(
            [[x/1000],
            [y/1000],[0]])
        R=np.array(
            [[np.cos(th),-np.sin(th),0],
            [np.sin(th),np.cos(th),0],
            [0,0,1]])
        Y=np.dot(R,X+B)
        return list(Y)

    def processReceivedData(sonarData):
        distanceList=sonarData.split('; ')
        distanceList=[float(i) for i in distanceList]
        return distanceList

    def runSonar(self):
        points=[]
        stamp=rospy.Time.now()
        self.odom_tf.sendTransform(
            (0,0,0),
            (0,0,0,0),
            stamp,
            'base_link',
            'odom',
        )

        self.serial.write(b"SA\n")
        time.sleep(0.001)

        x=self.serial.readline().decode('UTF-8')
        distances=self.processReceivedData(x)
        dIndex=0
        for d in distances:
            X=self.sonarPos[dIndex]['X']
            Y=self.sonarPos[dIndex]['y']
            Th=self.sonarPos[dIndex]['th']
            obstacle=self.transform(d,X,Y,Th)
            points.append(Point32(obstacle[0],obstacle[1],obstacle[2]))
            dIndex+=1
        
        points.pop()
        cloud=PointCloud()
        cloud.header.stamp=stamp
        cloud.header.frame_id='odom'
        cloud.points=points
        self.publisher.publish(cloud)
        time.sleep(0.1)

#-------------------------------------------------------------------------------

sonar = Sonar();
sonar.initPos();
sonar.initRos();
while 1:
    sonar.runSonar();
