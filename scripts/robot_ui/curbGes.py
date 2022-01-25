from tkinter import *


class CurbGes():
    def __init__(self, win, client):
        self.__win = win
        self.__client = client
        self.__height = 0
        self.__width = 0
        self.setSize(450, 350)
        self.setInterface()
        pass

    def setInterface(self):
        savingFrame = LabelFrame(self.__win, text='Enregistrement')
        savingFrame.pack()
        curbFrame = LabelFrame(self.__win, text='Courbes')
        curbFrame.pack()

        #enregistrement
        beginSavingButton = Button(savingFrame, text="Commmencer l'enregistrement")
        beginSavingButton.grid(row=1, columnspan= 3, column=1, sticky="we", padx=10, pady=10)

        fileNameEntry = Entry(savingFrame)
        fileNameEntry.grid(row=2, columsetInterfacen=1, sticky="we", padx=5, pady=5)

        saveButton = Button(savingFrame, text="Enregistrer")
        saveButton.grid(row=2, column=2, sticky="we", padx=5, pady=5)

        infoLabel = Label(savingFrame, text="Arrêt")
        infoLabel.grid(row=2, column=3, sticky="we", padx=5, pady=5)

        #courbes
        curbLabel = Label(curbFrame, text="Liste des courbes: ")
        curbLabel.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
    def setSize(self, w, h):
        self.__height = h
        self.__width = w
        self.__win.geometry(str(w)+'x'+str(h))
