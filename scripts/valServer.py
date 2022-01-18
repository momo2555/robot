#!/usr/bin/env python
import rospy
import asyncio
import websockets
import math
import json
from nav_msgs.msg import Odometry

position = {
    x: 0,
    y: 0,
    th: 0
} #x,y, theta


async def echo(websocket):
    async for message in websocket:
        print(message)
        pos = {
            position : position
        }
        print(son.dumps(pos))
        await websocket.send(son.dumps(pos))

async def main():
    #run the server
    async with websockets.serve(echo, "localhost", 3223):
        await asyncio.Future()  # run forever

    #init Ros node

    rospy.Subscriber("enc_velocity", Odometry, getRobotpos)
    rospy.spin()

def getRobotPos(pos):
    position.x = pos.pose.pose.x
    position.y = pos.pose.pose.y
    position.th = math.atan2(math. pos.pose.orientation.z, pos.pose.orientation.w)



asyncio.run(main())