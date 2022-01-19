import numpy as np

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
