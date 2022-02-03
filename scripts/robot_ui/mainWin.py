from tkinter import *
from clientThread import *
from robot import Robot
from field import Field
from clientThread import serverMsg
from motorProp import MotorProp
from curbGes import CurbGes
from testAsserv import TestAsserv


class MainWin(Tk):
	def __init__(self,client, w=1000, h=800):
		Tk.__init__(self)
		self.__height = h
		self.__width  = w
		self.__client = client
		self.setSize(w, h)
		self.setInterface()
		#initialisation du thread de réccupération de la position
		self.__getInterfacePos = GetPositionThread(client)
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

		#bouton pour commencer l'essai en boucle ouverte
		startOpenLoopButton = Button (rightSide, text = "Tester l'asservissement du robot")
		startOpenLoopButton.pack()
		startOpenLoopButton.bind('<Button-1>', self.showAsservTest)

		showCurbs = Button(rightSide, text = "Gestionnaire des courbes")
		showCurbs.pack()
		showCurbs.bind('<Button-1>', self.showCurbGes)

		openMotorProp = Button(rightSide, text = "Propriétés de la carte motor")
		openMotorProp.pack()
		openMotorProp.bind('<Button-1>', self.showMotorProp)

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

	
	def showCurbs(self, e):
		self.__robot.showCurb()
		pass

	def beginMonitor(self, e):
		self.__robot.initCurb()
		pass
	

	def showMotorProp(self, e):
		MotorProp(Toplevel(self), self.__client)
	
	def showAsservTest(self, e):
		TestAsserv(Toplevel(self), self.__client)
	def showCurbGes(self, e):
		CurbGes(Toplevel(self), self.__client, self)

	
	def startCurbMonitoring(self, curb):
		self.__robot.setCurb(curb)
