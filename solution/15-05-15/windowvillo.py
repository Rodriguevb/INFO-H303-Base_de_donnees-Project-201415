#!/usr/bin/python
# -*- coding:utf-8 -*-

from tkinter import *

class WindowVillo(Frame):
    def __init__(self,master=None):
        """ Constructeur """
        Frame.__init__(self,master, height=600, width=800)
        self.page = ""
        self.__makeHomepage()
        
    def __packFrame(self):
        """ affiche la frame """
        self.pack_propagate(False)
        self.pack()

    def __makeHomepage(self):
        """ Dessine la page d'accueil """
        self.__destroyPage()
        
        self.page = "homepage"

        self.hptitle = Label(self, text= " Villo Manager : ")
        self.consultButton = Button(self,
                               text="Consulter les stations et les Villos",
                               width=50,
                                command=self.__makeConsultpage)
        self.registerButton = Button(self,
                                text="S'enregistrer",
                                width=50)
        self.connectButton = Button(self,
                               text="Se connecter",
                               width=50)

        self.hptitle.place(x=350,y=200)
        self.consultButton.place(x=210,y=250)
        self.registerButton.place(x=210,y=300)
        self.connectButton.place(x=210,y=350)
        self.__packFrame()

    def __destroyPage(self):
        """ Détruit la page actuelle """
        if ( self.page == "homepage" ):
            self.__destroyHomepage()
        elif ( self.page == "consult" ):
            self.__destroyConsultpage()
        self.page = ""

    def __destroyHomepage(self):
        """ Détruit la page d'accueil """
        self.hptitle.destroy()
        self.consultButton.destroy()
        self.registerButton.destroy()
        self.connectButton.destroy()

    def __makeConsultpage(self):
        """ Dessine la page de consultation """
        self.__destroyPage()
        self.page = "consult"

        self.listStation = Listbox(self,
                                   width=35,
                                   height=30)

        self.listVillo = Listbox(self,
                                   width=35,
                                   height=30)
        
        self.buttonVillo = Button(self,
                             text="Voir les villos")

        self.buttonBack = Button(self,
                                 text="Retour",
                                 command=self.__makeHomepage)

        self.listStation.insert(END,"test")

        self.listVillo.insert(END,"test")
        
        self.listStation.place(x=50,y=20)
        self.listVillo.place(x=500, y=20)
        self.buttonVillo.place(x=350, y=250)
        self.buttonBack.place(x=50,y=550)

    def __destroyConsultpage(self):
        """ Détruit la page de consultation """
        self.listStation.destroy()
        self.listVillo.destroy()
        self.buttonVillo.destroy()
        self.buttonBack.destroy()
        
