import numpy as np
import matplotlib.pyplot as plt
import time 

class Robot():
	def __init__(self, field, x = 0, y = 0,th = 0.7):
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
		self.__diffSpeed = [0, 0]
		self.__cons = [0, 0]

		self.__T = []
		self.__Xx = []
		self.__Xy = []
		self.__Vl = []
		self.__Vr = []
		self.__Cl = []
		self.__Cr = []
		self.__cid = 0
		self.__time = time.time()
		
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
		
		if(data["type"]=="position"):
			self.__x = data["position"]["x"]*100
			self.__y = data["position"]["y"]*100
			self.__th = data["position"]["th"]
			
			self.__diffSpeed = [ data["diffSpeed"]["left"], data["diffSpeed"]["right"] ]
			self.__cons = [data["cons"]["left"], data["cons"]["right"]]
			#redessiner e terrain (la fonction de dessin du robot sera appeler automatiquement)
			self.__field.drawLandMark()
			
			#enregistrement des données
			self.__T.append(time.time() - self.__time )
			self.__Xx.append(self.__x)
			self.__Xy.append(self.__y)
			self.__Vl.append(self.__diffSpeed[0])
			self.__Vr.append(self.__diffSpeed[1])
			self.__Cl.append(self.__cons[0])
			self.__Cr.append(self.__cons[1])


		pass

	def initCurb(self):
		self.__time = time.time()
		self.__T = []
		self.__Xx = []
		self.__Xy = []
		self.__Vl = []
		self.__Vr = []
		self.__Cl = []
		self.__Cr = []

	def showCurb(self):
		fig = plt.figure()
		fig.add_subplot(121)
		plt.plot(self.__T, self.__Cl)
		plt.plot(self.__T, self.__Vl)
		fig.add_subplot(122)
		plt.plot(self.__T, self.__Cr)
		plt.plot(self.__T, self.__Vr)
		plt.show()
		#ecrire dans un fichier le résultat
		f = open("courbe-" + str(self.__cid) + ".csv", "w")
		self.__cid+=1
		for i in range(len(self.__T)):
			f.write(str(self.__T[i]) + "," + str(self.__Cl[i]) + "," + str(self.__Cr[i]) + "," 
			+ str(self.__Vl[i]) + "," + str(self.__Vr[i]) + "\n")
		f.close()
		pass
