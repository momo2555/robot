from tkinter import *
from turtle import width
from clientThread import serverMsg
class MotorProp():
    def __init__(self, win, client):
        self.__win = win
        self.__client = client
        self.__height = 0
        self.__width = 0
        self.setSize(750, 450)
        self.setInterface()
    
    def setInterface(self):
        titreLabel = Label(self.__win, text='Proprités de la carte moteur')
        titreLabel.grid(column=1, row=1, sticky="we", columnspan=6, padx=5, pady=5)
        
        #left pid
        leftPIDLabel = Label(self.__win, text='PID gauche :')
        leftPIDLabel.grid(column=1, row=2, sticky="we", columnspan=2, padx=5, pady=5)

        lkpLabel = Label(self.__win, text='Kp')
        lkpLabel.grid(column=1, row=3, sticky="e", padx=3, pady=3)

        lkiLabel = Label(self.__win, text='Ki')
        lkiLabel.grid(column=3, row=3, sticky="e", padx=3, pady=3)

        lkdLabel = Label(self.__win, text='Kd')
        lkdLabel.grid(column=5, row=3, sticky="e", padx=3, pady=3)

        self.__lkpEntry = Entry(self.__win)
        self.__lkpEntry.grid(column=2, row=3, sticky="we", padx=3, pady=3)

        self.__lkiEntry = Entry(self.__win)
        self.__lkiEntry.grid(column=4, row=3, sticky="we", padx=3, pady=3)

        self.__lkdEntry = Entry(self.__win)
        self.__lkdEntry.grid(column=6, row=3, sticky="we", padx=3, pady=3)

        #save button
        applyLeftPidButton = Button(self.__win, text = "Enregistrer")
        applyLeftPidButton.bind('<Button-1>', self.applyLeftPidChanges)
        applyLeftPidButton.grid(column=6, row=4, columnspan=3, sticky="we", padx=7, pady=7)

        #left pid
        rightPIDLabel = Label(self.__win, text='PID droite :')
        rightPIDLabel.grid(column=1, row=5, sticky="we" , columnspan=2, padx=5, pady=5)

        rkpLabel = Label(self.__win, text='Kp')
        rkpLabel.grid(column=1, row=6, sticky="e", padx=3, pady=3)

        rkiLabel = Label(self.__win, text='Ki')
        rkiLabel.grid(column=3, row=6, sticky="e", padx=3, pady=3)

        rkdLabel = Label(self.__win, text='Kd')
        rkdLabel.grid(column=5, row=6, sticky="e", padx=3, pady=3)

        self.__rkpEntry = Entry(self.__win)
        self.__rkpEntry.grid(column=2, row=6, sticky="we", padx=3, pady=3)

        self.__rkiEntry = Entry(self.__win)
        self.__rkiEntry.grid(column=4, row=6, sticky="we", padx=3, pady=3)

        self.__rkdEntry = Entry(self.__win)
        self.__rkdEntry.grid(column=6, row=6, sticky="we", padx=3, pady=3)

        #save button
        applyRightPidButton = Button(self.__win, text = "Enregistrer")
        applyRightPidButton.bind('<Button-1>', self.applyRightPidChanges)
        applyRightPidButton.grid(column=6, row=7, columnspan=3, sticky="we", padx=7, pady=7)

        #gain moteurs
        motorGainLabel = Label(self.__win, text='Gain moteur')
        motorGainLabel.grid(column=1, row=8, sticky="e" , columnspan=2, padx=5, pady=5)

        powerKleftLabel = Label(self.__win, text='Gain gauche : ')
        powerKleftLabel.grid(column=1, row=9, sticky="e", padx=3, pady=3)

        powerKrightLabel = Label(self.__win, text='Gain droite : ')
        powerKrightLabel.grid(column=3, row=9, sticky="we", padx=3, pady=3)

        self.__powerKleftEntry = Entry(self.__win)
        self.__powerKleftEntry.grid(column=2, row=9, sticky="we", padx=3, pady=3)

        self.__powerKrightEntry = Entry(self.__win)
        self.__powerKrightEntry.grid(column=4, row=9, sticky="we", padx=3, pady=3)

        #save button
        applyKpowerButton = Button(self.__win, text = "Enregistrer")
        applyKpowerButton.bind('<Button-1>', self.applyKpowerhanges)
        applyKpowerButton.grid(column=6, row=10, columnspan=3, sticky="we", padx=7, pady=7)

        #gain moteurs
        measureGainLabel = Label(self.__win, text='Gain mesure')
        measureGainLabel.grid(column=1, row=11, sticky="e" , columnspan=2, padx=5, pady=5)

        measureKleftLabel = Label(self.__win, text='Gain gauche : ')
        measureKleftLabel.grid(column=1, row=12, sticky="e", padx=3, pady=3)

        measureKrightLabel = Label(self.__win, text='Gain droite : ')
        measureKrightLabel.grid(column=3, row=12, sticky="we", padx=3, pady=3)

        self.__measureKleftEntry = Entry(self.__win)
        self.__measureKleftEntry.grid(column=2, row=12, sticky="we", padx=3, pady=3)

        self.__measureKrightEntry = Entry(self.__win)
        self.__measureKrightEntry.grid(column=4, row=12, sticky="we", padx=3, pady=3)

        #save button
        applyKmeasureButton = Button(self.__win, text = "Enregistrer")
        applyKmeasureButton.bind('<Button-1>', self.applyKmeasureChanges)
        applyKmeasureButton.grid(column=6, row=13, columnspan=3, sticky="we", padx=7, pady=7)

        

    def setSize(self, w, h):
        self.__height = h
        self.__width = w
        self.__win.geometry(str(w)+'x'+str(h))
       
        
        

    def applyLeftPidChanges(self, e):
        #send left values
        msg = serverMsg()
        msg.setMotorrequest("set_pid_left")
        msg.addParam("p", float(self.__lkpEntry.get()))
        msg.addParam("i", float(self.__lkiEntry.get()))
        msg.addParam("d", float(self.__lkdEntry.get()))
        self.__client.sendMsg(msg.toObject())
        pass
    
    def applyRightPidChanges(self, e):
        #send right values
        msg = serverMsg()
        msg.setMotorrequest("set_pid_right")
        msg.addParam("p", float(self.__rkpEntry.get()))
        msg.addParam("i", float(self.__rkiEntry.get()))
        msg.addParam("d", float(self.__rkdEntry.get()))
        self.__client.sendMsg(msg.toObject())
        pass

    def applyKpowerhanges(self, e):
        #send gains
        msg = serverMsg()
        msg.setMotorrequest("set_power_k")
        msg.addParam("l", float(self.__powerKleftEntry.get()))
        msg.addParam("r", float(self.__powerKrightEntry.get()))
        self.__client.sendMsg(msg.toObject())
        pass

        pass
    
    def applyKmeasureChanges(self, e):
        msg = serverMsg()
        msg.setMotorrequest("set_measure_k")
        msg.addParam("l", float(self.__measureKleftEntry.get()))
        msg.addParam("r", float(self.__measureKrightEntry.get()))
        self.__client.sendMsg(msg.toObject())
        pass
        pass