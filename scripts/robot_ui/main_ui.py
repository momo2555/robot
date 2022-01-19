#!/usr/bin/env python3
from http.client import OK
from tkinter import *
import numpy as np
import rospy
from threading import Thread
from geometry_msgs.msg import PoseStamped
import re
import asyncio
import websocket
import json
import math
import time
import socket
""" root = Tk()
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
root.mainloop() """

#on ne peut pas appeler spin() de rospy et mainLoop() de tkinter au même temps
#on créé donc un thread pour éxecuter rospy.spin()

class MainWin(Tk):
	def __init__(self,client, w=1000, h=800):
		Tk.__init__(self)
		self.__height = h
		self.__width = w
		self.__client = client
		self.setSize(w, h)
		self.setInterface()
		#initialisation du thread de réccupération de la position
		self.__getInterfacePos = GetPositionThread()
		self.__getInterfacePos.start()
		
		
	def setSize(self, w, h):
		self.__height = h
		self.__width = w
		self.geometry(str(w)+'x'+str(h))
		
	def mainLoop(self):
		self.mainloop()
    
	def getCoord(self):
		lst = [self.__width,self.__height]
		return lst

	def setInterface(self):
		pan = PanedWindow(self, handlesize=8, showhandle=False, sashrelief='sunken', orient=VERTICAL)
		
		pan.pack(fill=BOTH, expand=2)
		toptSide = PanedWindow(self, handlesize=8, showhandle=False, sashrelief='sunken')
		bottomtSide = Frame(pan, bg="red")
		leftSide = Frame(toptSide, bg="blue")
		rightSide = Frame(toptSide, bg = "yellow")
		toptSide.add(leftSide)
		toptSide.add(rightSide)
		pan.add(toptSide)
		pan.add(bottomtSide)

		self.__field = Field(leftSide)
		self.__field.pack(padx=10, pady=10, fill=BOTH, expand=1)
		#self.__field.grid(column=1, row=1, sticky="new")
		#pan.grid(row=1, column=1, sticky="ewns")
		self.__robot = Robot(self.__field)
		self.title('Robot IHM')
		
		self.__robot.drawRobot()
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(1, weight=1)
		

	def robotGetData(self):
		self.__client.onReceive(self.__robot.setFromServer)
		pass
	

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

class Field(Canvas):
	def __init__(self, parent):
		Canvas.__init__(self, parent, background="white")
		self.__backgroundColor = "white"
		#self.grid(row=0, column=3, columnspan=50, rowspan=5)
		self.__origin = [110, 100] #en pixel
		self.__r = 2 #coefficient de réduction (à appliquer aux valeurs centimètriques)
		self.__inter = 20 #inter en cm
		self.__fieldPos = [0, 0] #en pixel
		self.__showLandmark = True
		self.drawLandMark()
		#move the interface
		self.__lastOrigin = [0, 0]
		self.__mousePos = [0, 0]
		self.__canMove = False
		#events:
		self.bind("<Configure>", self.sizeChanged)
		self.bind("<Motion>", self.mouseMove)
		self.bind("<ButtonPress>", self.mouseDown)
		self.bind("<ButtonRelease>", self.mouseUp)
		self.bind("<MouseWheel>", self.mouseWheel)
		
		
		
		

	
	#réccupéraion d'un vecteur de coordonnées de l'origine
	def getOrigin(self):
		return np.array([[self.__origin[0]],
						[self.__origin[1]]])
	def drawLandMark(self, delete=True):
		
		if delete:
			self.delete("all")
		if(self.__showLandmark):
			#get size info
			g = re.split('x|\+', self.winfo_geometry())
			w = int(g[0])
			h = int(g[1])
			#axe vertical:
			self.create_line((self.__origin[0], 0), (self.__origin[0], h), fill="red", width=2)
			#axe horizontal:
			self.create_line((0, self.__origin[1]), (w, self.__origin[1]), fill="red", width=2)

			sdw = w - self.__origin[0]
			sdh = h - self.__origin[1]
			if (sdw < w ) :
				ww =self.__origin[0]
				while ww >0:
					ww-=self.__r*self.__inter
					self.create_line((ww, 0), (ww, h), fill="red", width=1)

			if (sdw > 0):
				ww =  self.__origin[0]
				while ww < w:
					ww+=self.__r*self.__inter
					self.create_line((ww, 0), (ww, h), fill="red", width=1)
				

			if (sdh < h ) :
				hh = self.__origin[1]
				while hh > 0:
					hh-=self.__r*self.__inter
					self.create_line((0, hh), (w, hh), fill="red", width=1)
				

			if(sdh > 0):
				hh =  self.__origin[1]
				while hh < h:
					hh+=self.__r*self.__inter
					self.create_line((0, hh), (w, hh), fill="red", width=1)
		#the field was been changed => raise ans event
		self.event_generate("<<FieldChanged>>")
	
	def getReduc(self):
		return self.__r

	def sizeChanged(self, event):
		#self.drawLandMark()
		
		self.drawLandMark()
		pass
	def mouseMove(self, event):
		if(self.__canMove):
			ox = self.__lastOrigin[0] + (event.x - self.__mousePos[0])
			oy = self.__lastOrigin[1] + (event.y - self.__mousePos[1])
			self.__origin = [ox, oy]
			self.drawLandMark()
		pass
	def mouseUp(self, event):
		self.__canMove = False
		pass
	def mouseDown(self, event):
		self.__mousePos = [event.x, event.y]
		self.__lastOrigin = self.__origin
		self.__canMove = True
		pass
	def mouseWheel(self, event):
		self.__r = event.num
		self.drawLandMark()

class Robot():
	def __init__(self, field:Field, x = 0, y = 0,th = 0.7):
		#le robot va être dessiné sur un canvas
		self.__x = x
		self.__y = y 
		self.__th = th #angle theta
		self.__color = "red"
		self.__field = field
		
		#  ------
		#  |    | 
		#  |   \| = a (face avant du robot)
		#  |   /|
		#  |    |
		#  ------ = b
		self.__a = 35 #cm
		self.__b = 20 #cm
		#self.__field.event_add("<<FieldChange>>", "<Motion>", "<Configure>", "<MouseWheel>",)
		self.__field.bind("<<FieldChanged>>", self.fieldChange)
		
		
	def drawRobot(self):
		#rapport de reduction
		r = self.__field.getReduc()
		#liste des points
		
		#premier rectangle
		a = self.__a*r
		b = self.__b*r
		X = [
			np.array([[-b/2], [-a/2]]), 
			np.array([[b/2] , [-a/2]]),
			np.array([[b/2] , [a/2]]),
			np.array([[-b/2], [a/2]]),
		]
		#use the last coor to drw point to point
		lines = [[0, 1, 2, 3, 0]]
		#creating translate version
		B = np.array([[self.__x*r], [-self.__y*r]])
		#creating a rotation vector
		th = self.__th
		A = np.array([[np.cos(th), -np.sin(th)],
				 	 [np.sin(th),  np.cos(th)]])
		#translate to origin
		O = self.__field.getOrigin()		
		Y = []
		for x in X:
			Y.append(np.dot(A, x) + B + O)
		#drw on the canvas
		for l in lines:
			for i in range(len(l) - 1):
				self.__field.create_line((Y[l[i]][0,0], Y[l[i]][1,0]),(Y[l[i+1]][0,0], Y[l[i+1]][1,0]) ,fill=self.__color, width=2)
		
	def fieldChange(self, event):
		self.drawRobot()

	def setFromServer(self, data):
		print(data)
		if(data["type"]=="position"):
			self.__x = data["position"]["x"]*100
			self.__y = data["position"]["y"]*100
			self.__th = data["position"]["th"]
			#redessiner e terrain (la fonction de dessin du robot sera appeler automatiquement)
			self.__field.drawLandMark()
		pass

class GetPositionThread(Thread):
	def __init__(self):
		Thread.__init__(self)
	
	def run(self):
		print("start position getter thread")
		while True:
			#create a new request
			rqt = serverMsg()
			rqt.setRequest("get_position")
			#send request
			client.sendMsg(rqt.toObject())
			time.sleep(0.1)


class serverMsg():
	def __init__(self):
		self.__type = "request"
		self.__request = "none"
	def setRequest(self, request):
		self.__request = request
		self.__type = "request"

	def toObject(self):
		return {
			"type" : self.__type,
			"request" : self.__request
		}
	def toString(self):
		return json.dumps( self.toObject() )

class ClientSocket(Thread):
	def __init__(self):
		self.__client =socket.socket(
    				socket.AF_INET, socket.SOCK_STREAM)
		self.__callbacks = []
		#initialisation du client websocket
		Thread.__init__(self)
		
		
	

	def run(self):
		self.__client.connect(('192.168.236.11', 32233))
		print("démarrage du client")
		while True:
			response = self.__client.recv(1024)
			print(response)
			#fetch callbacks
			for callback in self.__callbacks:
				callback(json.loads(response.decode('utf8')))
		
	def sendMsg(self, objMsg):
		self.__client.send(json.dumps( objMsg ).encode('utf8'))
	def onReceive(self, callback):
		self.__callbacks.append(callback)
	



client = ClientSocket()
client.start()




print("lancement de l'interface graphique")
mainWin = MainWin(client)
mainWin.robotGetData()
mainWin.mainLoop()
