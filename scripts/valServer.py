#!/usr/bin/env python
import rospy
import asyncio
import websockets
import math
import json
from nav_msgs.msg import Odometry

position = {
    "x": 0,
    "y": 0,
    "th": 0
} #x,y, theta


async def echo(websocket):
    async for message in websocket:
        print(message)
        req = {
            "type" : "position"
            "position" : position
        }
        print(son.dumps(req))
        await websocket.send(son.dumps(req))

async def main():
    #run the server
    print("initialisation du serveur websocket")
    server = websockets.serve(echo, "localhost", 3223)

    
async def rosInit():
    print("initialisation noeud serialCon")
    rospy.init_node('serialCon')
    #init Ros node
    print("initialisation du subscriber")
    rospy.Subscriber("enc_velocity", Odometry, getRobotPos)
    await rospy.spin()

def getRobotPos(pos):
    position["x"] = pos.pose.pose.position.x
    position["y"] = pos.pose.pose.position.y
    position["th"] = math.atan2(pos.pose.pose.orientation.z, pos.pose.pose.orientation.w)
    #print(position)   


asyncio.run(main())
asyncio.run(rosInit())
