from cProfile import label
import matplotlib.pyplot as plt
import time
import os

class Curb ():
    def __init__(self) -> None:
        self.initCurb()
        self.__path = ""
        self.__monitoring = False
        self.__time = time.time()
        self.__name = ""
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

    def plot(self):
        """fig = plt.figure()
        
        fig.add_subplot(121)
        plt.plot(self.__T, self.__Cl, label="Consigne")
        plt.plot(self.__T, self.__Vl, label="Réponse")
        
        fig.add_subplot(122)
        plt.plot(self.__T, self.__Cr, label="Consigne")
        plt.plot(self.__T, self.__Vr, label="Réponse")"""
        

        fig, axs = plt.subplots(1, 2, constrained_layout=True)
        axs[0].plot(self.__T, self.__Cl)
        axs[0].plot(self.__T, self.__Vl)
        axs[0].set_title('Roue gauche')
        axs[0].set_xlabel('temps (s)')
        axs[0].set_ylabel('vitesse')
        
        fig.suptitle(self.__name, fontsize=16)
        
        axs[1].plot(self.__T, self.__Cr, label="Consigne")
        axs[1].plot(self.__T, self.__Vr, label="Réponse")
        axs[1].set_title('Roue droite')
        axs[1].set_xlabel('temps (s)')
        axs[1].set_ylabel('Vitesse')
        plt.show()
        pass

    def open(self, path):
        self.__path = path
        self.initCurb()
        F = open(path)
        for l in F:
            columns = l.split(',')
            self.__T. append(float (columns[0]))
            self.__Cl.append(float(columns[1]))
            self.__Cr.append(float(columns[2]))
            self.__Vl.append(float(columns[3]))
            self.__Vr.append(float(columns[4]))
        F.close()

    def save(self, path=None):
        if path != None:
            self.__path = path
        f = open(path, "w")
        for i in range(len(self.__T)):
            f.write(str(self.__T[i]) + "," + str(self.__Cl[i]) + "," + str(self.__Cr[i]) + "," 
            + str(self.__Vl[i]) + "," + str(self.__Vr[i]) + "\n")
        f.close()

    def setPath(self, path):
        self.__path = path

    def addT(self, t, byRef = True):
        if byRef:
            self.__T.append(t - self.__time)
        else:
            self.__T.append(t)
    
    def addX(self, x, y):
        self.__Xx.append(x)
        self.__Xy.append(y)
    
    def addV(self, l, r):
        self.__Vl.append(l)
        self.__Vr.append(r)

    def addC(self, l, r):
        self.__Cl.append(l)
        self.__Cr.append(r)

    def startMonitoring(self):
        self.__monitoring = True
    
    def stopMonitoring(self):
        self.__monitoring = False
    
    def ifMonitoring(self):
        return self.__monitoring

    def setName(self, name):
        self.__name = name

    def getName(self):
        return self.__name