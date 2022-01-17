#!/USI/usr/bin/env python3
#!/usr/bin/env python
# license removed for brevity
import tf
import numpy as np 
import time 
import serial
import rospy
from std_msgs.msg import String 
from sensor_msgs.msg import PointCloud, ChannelFloat32
from geometry_msgs.msg import Point32
from tf2_ros.buffer_interface import Stamped
import yaml

def transform(d,x,y,th) :
    X=np.array([[d/1000],[0],[0]])
    B=np.array([[x/1000],[y/1000],[0]])
    R=np.array([[np.cos(th),-np.sin(th),0],
                [np.sin(th),np.cos(th),0],
                [0,0,1]])
    Y=np.dot(R,X+B)
    return list(Y)

def processReceivedData(sonarData):
    distanceList=sonarData.split('; ')
    distanceList=[float(i) for i in distanceList]
    #print(distanceList)
    return distanceList

ser = serial.Serial(port='/dev/ttyUSB0',baudrate = 115200)
stream=open("/home/loic/catkin_ws/src/sonar/config/sonar_config.yaml",'r')
data=yaml.load(stream)
sonarPos=data.items()
for key,value in sonarPos :
    if key=="sonars" :
        sonarPos=value 
#print(sonarPos)

pub = rospy.Publisher('sonartopic', PointCloud, queue_size=10)
odom_tf=tf.TransformBroadcaster()
rospy.init_node('talker', anonymous=True)

while 1:
    points=[]
    stamp=rospy.Time.now()
    odom_tf.sendTransform(
        (0,0,0),
        (0,0,0,0),
        stamp,
        'base_link',
        'odom',
    )

    #print(cloud)

    ser.write(b"SA\n")
    time.sleep(0.001)
    x=ser.readline().decode('UTF-8')
    distances=processReceivedData(x)
    dIndex=0
    for d in distances:
        X=sonarPos[dIndex]['X']
        Y=sonarPos[dIndex]['y']
        Th=sonarPos[dIndex]['th']
        obstacle=transform(d,X,Y,Th)
        points.append(Point32(obstacle[0],obstacle[1],obstacle[2]))
        dIndex+=1
    #print(points)
    cloud=PointCloud()
    cloud.header.stamp=stamp
    cloud.header.frame_id='odom'
    cloud.points=points
    pub.publish(cloud)
    #print(x)
    time.sleep(0.1)
