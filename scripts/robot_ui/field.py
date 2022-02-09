from tkinter import *
import numpy as np
import re

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
        # Move the interface
        self.__lastOrigin = [0, 0]
        self.__mousePos = [0, 0]
        self.__canMove = False
        # Events:
        self.bind("<Configure>", self.sizeChanged)
        self.bind("<Motion>", self.mouseMove)
        self.bind("<ButtonPress>", self.mouseDown)
        self.bind("<ButtonRelease>", self.mouseUp)
        self.bind("<MouseWheel>", self.mouseWheel)
    
    # Réccupéraion d'un vecteur de coordonnées de l'origine
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