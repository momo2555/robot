#!/usr/bin/env python3
from http.client import OK
import numpy as np
from tkinter import *
from mainWin import MainWin
import rospy
from threading import Thread
from geometry_msgs.msg import PoseStamped
import re
from clientThread import *
import asyncio
import json
import math
import time
import socket
""" 
root = Tk()
width = 400
heigh = 400
param_a_entrer = str(width)+"x"+str(heigh)
root.geometry(param_a_entrer)        
txt = Label(root, text = "test")
txt.grid(column = 0, row = 0)

def test():
    print("test")
    
bouton = Button(root, text = 'test' , command = test())
bouton.grid()
root.mainloop()
"""

# On ne peut pas appeler spin() de rospy et mainLoop() de tkinter en même temps
# On créé donc un thread pour éxecuter rospy.spin()


""""
class Bouton(Button):
    def __init__(self, win, txt = '', cmd = None, x = 10, y = 10):
        self.win = win
        self.txt = txt
        self.cmd = cmd
        self.x = x
        self.y = y
        #Button(win,text = txt, command = cmd)
        
    def replace(self,x,y):
        self.place(x,y)
"""

client = ClientSocket()
client.start()

print("Lancement de l'interface graphique")
mainWin = MainWin(client)
mainWin.robotGetData()
mainWin.mainLoop()
