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
        titreLabel.grid(column=1, row=1, sticky="we", columnspan=6, padx=25, pady=25)
        
        #left pid
        leftPIDLabel = Label(self.__win, text='PID gauche :')
        leftPIDLabel.grid(column=1, row=2, sticky="we", columnspan=2, padx=15, pady=15)

        lkpLabel = Label(self.__win, text='Kp')
        lkpLabel.grid(column=1, row=3, sticky="we", padx=5, pady=5)

        lkiLabel = Label(self.__win, text='Ki')
        lkiLabel.grid(column=3, row=3, sticky="we", padx=5, pady=5)

        lkdLabel = Label(self.__win, text='Kd')
        lkdLabel.grid(column=5, row=3, sticky="we", padx=5, pady=5)

        self.__lkpEntry = Entry(self.__win)
        self.__lkpEntry.grid(column=2, row=3, sticky="we", padx=5, pady=5)

        self.__lkiEntry = Entry(self.__win)
        self.__lkiEntry.grid(column=4, row=3, sticky="we", padx=5, pady=5)

        self.__lkdEntry = Entry(self.__win)
        self.__lkdEntry.grid(column=6, row=3, sticky="we", padx=5, pady=5)

        #left pid
        rightPIDLabel = Label(self.__win, text='PID droite :')
        rightPIDLabel.grid(column=1, row=4, sticky="we" , columnspan=2, padx=15, pady=15)

        rkpLabel = Label(self.__win, text='Kp')
        rkpLabel.grid(column=1, row=5, sticky="we", padx=5, pady=5)

        rkiLabel = Label(self.__win, text='Ki')
        rkiLabel.grid(column=3, row=5, sticky="we", padx=5, pady=5)

        rkdLabel = Label(self.__win, text='Kd')
        rkdLabel.grid(column=5, row=5, sticky="we", padx=5, pady=5)

        self.__rkpEntry = Entry(self.__win)
        self.__rkpEntry.grid(column=2, row=5, sticky="we", padx=5, pady=5)

        self.__rkiEntry = Entry(self.__win)
        self.__rkiEntry.grid(column=4, row=5, sticky="we", padx=5, pady=5)

        self.__rkdEntry = Entry(self.__win)
        self.__rkdEntry.grid(column=6, row=5, sticky="we", padx=5, pady=5)

        #save button
        applyButton = Button(self.__win, text = "Appliquer les nouvelles propriétés")
        applyButton.bind('<Button-1>', self.applyChanges)
        applyButton.grid(column=6, row=6, columnspan=3, sticky="we", padx=15, pady=15)

    def setSize(self, w, h):
        self.__height = h
        self.__width = w
        self.__win.geometry(str(w)+'x'+str(h))

    def applyChanges(self, e):
        #send left values
        msg = serverMsg()
        msg.setMotorrequest("set_pid_left")
        msg.addParam("p", float(self.__lkpEntry.get()))
        msg.addParam("i", float(self.__lkiEntry.get()))
        msg.addParam("d", float(self.__lkdEntry.get()))
        self.__client.sendMsg(msg.toObject())

        #send left values
        msg = serverMsg()
        msg.setMotorrequest("set_pid_right")
        msg.addParam("p", float(self.__rkpEntry.get()))
        msg.addParam("i", float(self.__rkiEntry.get()))
        msg.addParam("d", float(self.__rkdEntry.get()))
        self.__client.sendMsg(msg.toObject())

        pass