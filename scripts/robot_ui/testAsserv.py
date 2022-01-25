from inspect import FrameInfo
from tkinter import *
from tkinter.tix import NoteBook
from clientThread import serverMsg
class TestAsserv():
    def __init__(self, win, client):
        self.__win = win
        self.__client = client
        self.__height = 0
        self.__width = 0
        self.setSize(450, 350)
        self.setInterface()
    
    def setInterface(self):
        
        openLoopFrame = LabelFrame(self.__win)
        DiffSpeedFrame = LabelFrame(self.__win)
        openLoopFrame.grid(column=1, row=1, sticky="we", pady=10, padx=10)
        DiffSpeedFrame.grid(column=1, row=2, sticky="we", pady=10, padx=10)
        
        #Test en boucle ouverteboucle ouverte
        openLoopLabel = Label(openLoopFrame, text="Boucle ouverte : ")
        openLoopLabel.grid(row=1, columnspan=2, column=1, sticky="we", pady=5, padx=5)
        stageTimeLabel = Label(openLoopFrame, text="Temps d'éxecution par étape")
        stageTimeLabel.grid(row=2, columnspan=1, column=1, sticky="we", pady=5, padx=5)

        self.__stageTimeSpinbox = Spinbox(openLoopFrame, format="%.3f", increment=0.01 )
        self.__stageTimeSpinbox.grid(row=2, column=2, sticky="we" , pady=5, padx=5)

        stageTimeSecondLabel = Label(openLoopFrame, text="s")
        stageTimeSecondLabel.grid(row=2, column=3, sticky="we", pady=5, padx=5)

        openLoopButton = Button(openLoopFrame, text="Lancer le test ! ")
        openLoopButton.bind('<Button-1>', self.startOpenLoop)
        openLoopButton.grid(row = 3, column=1, columnspan=2, sticky="we", pady=5, padx=5)
        #Test en boucle fermée

        diffSpeedLabel = Label(DiffSpeedFrame, text="Boucle fermée : ")
        diffSpeedLabel.grid(row=1, columnspan=2, column=1, sticky="we", pady=5, padx=5)
        durationLabel = Label(DiffSpeedFrame, text="Temps d'éxecution")
        durationLabel.grid(row=2, columnspan=1, column=1, sticky="we", pady=5, padx=5)

        self.__durationSpinbox = Spinbox(DiffSpeedFrame, format="%.3f", increment=0.01 )
        self.__durationSpinbox.grid(row=2, column=2, sticky="we", pady=5, padx=5 )
        

        durationSecondLabel = Label(DiffSpeedFrame, text="s")
        durationSecondLabel.grid(row=2, column=3, sticky="we", pady=5, padx=5)

        diffSpeedButton = Button(DiffSpeedFrame, text="Lancer le test ! ")
        diffSpeedButton.bind('<Button-1>', self.startDiffSpeed)
        diffSpeedButton.grid(row = 3, column=1, columnspan=2, sticky="we", pady=5, padx=5)

       
        pass

    def setSize(self, w, h):
        self.__height = h
        self.__width = w
        self.__win.geometry(str(w)+'x'+str(h))

    def startOpenLoop(self, e):
        print("open loop")
        rqt = serverMsg()
        rqt.setRequest("start_open_loop")
        rqt.addParam("stage_time", float(self.__stageTimeSpinbox.get()))
        self.__client.sendMsg(rqt.toObject())

    def startDiffSpeed(self, e):
        print("diff speed")
        rqt = serverMsg()
        rqt.setRequest("start_diff_speed")
        rqt.addParam("duration", float(self.__durationSpinbox.get()))
        self.__client.sendMsg(rqt.toObject())