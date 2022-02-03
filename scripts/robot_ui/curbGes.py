from distutils import filelist
from tkinter import *
import matplotlib.pyplot as plt
from curb import Curb
import os

class CurbGes():
    def __init__(self, win, client, parent):
        self.__parent = parent
        self.__win = win
        self.__client = client
        self.__height = 0
        self.__width = 0
        self.__selectedCurb = Curb()
        self.__monitoredCurb = Curb()
        self.setSize(450, 350)
        self.setInterface()
        pass

    def setInterface(self):
        savingFrame = LabelFrame(self.__win, text='Enregistrement')
        savingFrame.grid(column=1, row=1, sticky="we", padx=5, pady=5)
        curbFrame = LabelFrame(self.__win, text='Courbes')
        curbFrame.grid(column=1, row=2, sticky="we", padx=5, pady=5)


        #enregistrement
        self.__beginSavingButton = Button(savingFrame, text="Commmencer l'enregistrement")
        self.__beginSavingButton.bind('<Button-1>', self.startSaving)
        self.__beginSavingButton.grid(row=1, columnspan= 3, column=1, sticky="we", padx=10, pady=10)

        self.__fileNameEntry = Entry(savingFrame)
        self.__fileNameEntry.grid(row=2, column=1, sticky="we", padx=5, pady=5)

        saveButton = Button(savingFrame, text="Enregistrer")
        saveButton.bind('<Button-1>', self.SaveCurb)
        saveButton.grid(row=2, column=2, sticky="we", padx=5, pady=5)

        self.__infoLabel = Label(savingFrame, text="Arrêt")
        self.__infoLabel.grid(row=2, column=3, sticky="we", padx=5, pady=5)


        #courbes
        curbLabel = Label(curbFrame, text="Liste des courbes: ")
        curbLabel.grid(row=1, column=1, sticky="we", padx=5, pady=5)

        self.__curbsList = Listbox(curbFrame)
        self.__curbsList.grid(row=2, column=1, rowspan=3,sticky="we", padx=5, pady=5)
        self.listCurbs(None)

        refreshButton = Button(curbFrame, text="Rafraîchir")
        refreshButton.bind('<Button-1>', self.listCurbs)
        refreshButton.grid(row=2, column=2, sticky="we", padx=5, pady=5)
        
        showButton = Button(curbFrame, text="Voir la courbe")
        showButton.bind('<Button-1>', self.showCurb)
        showButton.grid(row=3, column=2, sticky="we", padx=5, pady=5)

        deleteButton = Button(curbFrame, text="Supprimer la courbe")
        #suppression bind
        deleteButton.grid(row=4, column=2, sticky="we", padx=5, pady=5)


    def setSize(self, w, h):
        self.__height = h
        self.__width = w
        self.__win.geometry(str(w)+'x'+str(h))

    def listCurbs(self, e):
        FileList = [ f for f in os.listdir('./curbs') if os.path.isfile(os.path.join('./curbs',f)) ]
        #ajouter tous les fichier à la listelistCurbs
        for file in FileList:
         self.__curbsList.insert('end', file)
        pass


    def showCurb(self, e):
        #reccupére la courbe slectionnée
        index = self.__curbsList.curselection()
        if len(index) > 0:
            index = index[0]
            #get file name
            fileName = self.__curbsList.get(index)
            self.__selectedCurb.open('curbs/' + fileName)
            self.__selectedCurb.plot()
        else:
            print("Vous n'avez pas sélectionner de courbes !")
        pass

    def startSaving(self, e):
       
        if not self.__monitoredCurb.ifMonitoring():
           
            self.__monitoredCurb.initCurb()
            self.__monitoredCurb.startMonitoring()
            self.__parent.startCurbMonitoring(self.__monitoredCurb)
            self.__infoLabel.config(text = "Enregistrement")
            self.__beginSavingButton.config(text="Arrêter l'enregistrment")
        else:
            self.StopSaving()
    
    def StopSaving(self):
        self.__monitoredCurb.stopMonitoring()
        #pas besoin d'envoyer l'info à toutes les unités d'enregistrement
        self.__infoLabel.config(text = "Arrêt")
        self.__beginSavingButton.config(text="Commencer l'enregistrment")

    def SaveCurb(self, e):
        self.__monitoredCurb.save('curbs/' + self.__fileNameEntry.get())

        