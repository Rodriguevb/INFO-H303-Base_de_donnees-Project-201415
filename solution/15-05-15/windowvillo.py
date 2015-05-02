#!/usr/bin/python
# -*- coding:utf-8 -*-

from tkinter import *
from VilloDatabase import *
from datetime import datetime

class WindowVillo(Frame):
    def __init__(self,master=None):
        """ Constructeur """
        Frame.__init__(self,master, height=600, width=800)
        self.page = ""
        self.connected = False
        self.__makeHomepage()

        self.db = VilloDatabase()
        
    def __packFrame(self):
        """ affiche la frame """
        self.pack_propagate(False)
        self.pack()

    def __makeHomepage(self):
        """ Dessine la page d'accueil """
        self.__destroyPage()
        self.page = "homepage"

        # On crée les widgets
        self.hptitle = Label(self, text= " Villo Manager : ")
        self.consultButton = Button(self,
                               text="Consulter les stations et les Villos",
                               width=50,
                                command=self.__makeConsultpage)
        self.registerButton = Button(self,
                                text="S'enregistrer",
                                width=50,
                                command=self.__makeRegistrypage)
        self.connectButton = Button(self,
                               text="Se connecter",
                               width=50,
                                command=self.__makeConnectpage)

        # On place les widgets
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
        elif ( self.page == "registry" ):
            self.__destroyRegistrypage()
        elif ( self.page == "connect" ):
            self.__destroyConnectpage()
        elif ( self.page == "manage"):
            self.__destroyManagepage()
        elif ( self.page == "villo"):
            self.__destroyVillopage()
        elif ( self.page == "history"):
            self.__destroyHistorypage()
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

        # On crée les widgets
        self.listStation = Listbox(self,
                                   width=35,
                                   height=30)

        self.listVillo = Listbox(self,
                                   width=35,
                                   height=30)
        
        self.buttonVillo = Button(self,
                             text="Voir les villos",
                             command=self.__loadVilloConsult)

        self.buttonBack = Button(self,
                                 text="Retour")

        # On change l'action du bouton de retour selon si on est connecté ou non.
        if self.connected:
            self.buttonBack.config(command=self.__makeManagepage)
        else:
            self.buttonBack.config(command=self.__makeHomepage)

        # On rempli la liste de station
        stationlist = self.db.getStationNameList()
        for station in stationlist:
            self.listStation.insert(END,station)
        
        # On place les widgets
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

    def __makeRegistrypage(self):
        """ Dessine la page d'enregistrement """
        self.__destroyPage()
        self.page = "registry"

        # Création widgets
        
        self.idEntry = Entry(self)
        self.idLabel = Label(self, text="ID :")

        self.passEntry = Entry(self, show="*")
        self.passLabel = Label(self, text="Mot de passe :")

        self.passValEntry = Entry(self, show="*")


        self.firstnameEntry = Entry(self)
        self.firstnameLabel = Label(self, text="Prénom :")

        self.nameEntry = Entry(self)
        self.nameLabel = Label(self, text="Nom :")

        self.phoneEntry = Entry(self)
        self.phoneLabel = Label(self, text="Téléphone :")

        self.cityEntry = Entry(self)
        self.cityLabel = Label(self, text="Ville :")

        self.cpEntry = Entry(self)
        self.cpLabel = Label(self, text="Code postal :")

        self.streetEntry = Entry(self)
        self.streetLabel = Label(self, text="Rue :")

        self.numberEntry = Entry(self)
        self.numberLabel = Label(self, text="Numéro :")

        self.cardEntry = Entry(self)
        self.cardLabel = Label(self, text="Carte bancaire :")

        self.registryButton = Button(self,
                                     text="S'enregistrer",
                                     width=40,
                                     command=self.__register)


        self.buttonBack = Button(self,
                                 text="Retour",
                                 command=self.__makeHomepage)


        # Placement widgets
        self.idEntry.place(x=420,y=70)
        self.idLabel.place(x=280,y=70)
        
        self.passEntry.place(x=420,y=100)
        self.passLabel.place(x=280,y=100)

        self.passValEntry.place(x=420,y=130)

        self.firstnameEntry.place(x=420,y=160)
        self.firstnameLabel.place(x=280,y=160)

        self.nameEntry.place(x=420,y=190)
        self.nameLabel.place(x=280,y=190)

        self.phoneEntry.place(x=420,y=220)
        self.phoneLabel.place(x=280,y=220)

        self.cityEntry.place(x=420,y=250)
        self.cityLabel.place(x=280,y=250)

        self.cpEntry.place(x=420,y=280)
        self.cpLabel.place(x=280,y=280)

        self.streetEntry.place(x=420,y=310)
        self.streetLabel.place(x=280,y=310)

        self.numberEntry.place(x=420,y=340)
        self.numberLabel.place(x=280,y=340)

        self.cardEntry.place(x=420, y=370)
        self.cardLabel.place(x=280, y=370)

        self.registryButton.place(x=280,y=420)

        self.buttonBack.place(x=50,y=550)


    def __destroyRegistrypage(self):
        """ Détruit la page d'enregistrement """
        self.idEntry.destroy()
        self.idLabel.destroy()
        
        self.passEntry.destroy()
        self.passLabel.destroy()

        self.passValEntry.destroy()

        self.firstnameEntry.destroy()
        self.firstnameLabel.destroy()

        self.nameEntry.destroy()
        self.nameLabel.destroy()

        self.phoneEntry.destroy()
        self.phoneLabel.destroy()

        self.cityEntry.destroy()
        self.cityLabel.destroy()

        self.cpEntry.destroy()
        self.cpLabel.destroy()

        self.streetEntry.destroy()
        self.streetLabel.destroy()

        self.numberEntry.destroy()
        self.numberLabel.destroy()

        self.cardEntry.destroy()
        self.cardLabel.destroy()

        self.registryButton.destroy()

        self.buttonBack.destroy()


    def __makeConnectpage(self):
        """ Dessine la page de connexion """
        self.__destroyPage()
        self.page = "connect"
        
        # Création widgets
        self.idEntry = Entry(self)
        self.idLabel = Label(self, text="ID :")

        self.passEntry = Entry(self,show="*")
        self.passLabel = Label(self, text="Mot de passe :")

        self.connectButton = Button(self,
                                     text="Se connecter",
                                     width=40,
                                    command=self.__connect)

        self.buttonBack = Button(self,
                                 text="Retour",
                                 command=self.__makeHomepage)


        # Placement widgets
        self.idEntry.place(x=420,y=200)
        self.idLabel.place(x=280,y=200)

        self.passEntry.place(x=420,y=230)
        self.passLabel.place(x=280,y=230)

        self.connectButton.place(x=280,y=300)

        self.buttonBack.place(x=50,y=550)

    def __destroyConnectpage(self):
        """ Détruit la page de connexion """
        self.idEntry.destroy()
        self.idLabel.destroy()
        self.passEntry.destroy()
        self.passLabel.destroy()
        self.connectButton.destroy()
        self.buttonBack.destroy()

    def __makeManagepage(self):
        """ Dessine la page de gestion """
        self.__destroyPage()
        self.page="manage"

        # Création widgets
        self.villoButton = Button(self,
                                 width=50,
                                 text="Prendre/Déposer Villo",
                                 command=self.__makeVillopage)

        self.consultButton = Button(self,
                                    width= 50,
                                    text="Consulter les stations et villo",
                                    command=self.__makeConsultpage)

        self.historyButton = Button(self,
                                    width=50,
                                    text="Consulter l'historique de mes déplacements",
                                    command=self.__makeHistorypage)

        self.problemButton = Button(self,
                                    width=50,
                                    text="Signaler un problème avec mon villo")

        self.disconnectButton = Button(self,
                                        text="Déconnexion",
                                        command=self.__disconnect)

        # placement des widgets
        self.villoButton.place(x=210,y=250)
        self.consultButton.place(x=210,y=300)
        self.historyButton.place(x=210,y=350)
        self.problemButton.place(x=210,y=400)
        self.disconnectButton.place(x=50,y=550)

    def __destroyManagepage(self):
        """ Détruit la page de gestion """
        self.villoButton.destroy()
        self.consultButton.destroy()
        self.historyButton.destroy()
        self.problemButton.destroy()
        self.disconnectButton.destroy()

    def __makeVillopage(self):
        """ Dessine la page de gestion de villo """
        self.__destroyPage()
        self.page = "villo"

        # Création widgets
        self.listStation = Listbox(self,
                                   width=35,
                                   height=30)

        stationlist = self.db.getStationNameList()
        for station in stationlist:
            self.listStation.insert(END,station)

        # TODO: Vérifier si l'utilisateur a déjà un Villo. Afficher les boutons en conséquences.
        hasVillo = self.db.isUserUsingVillo(self.uid)

        self.takeButton = Button(self,
                                width=30,
                                text="Prendre un villo",
                                command=self.__takeVillo)

        self.putButton = Button(self,
                                width=30,
                                text="Déposer un villo",
                                command=self.__putVillo)

        self.backButton = Button(self,
                                        text="Retour",
                                        command=self.__makeManagepage)

        # Placements widgets
        self.listStation.place(x=50,y=20)
        if not hasVillo:
            self.takeButton.place(x=400,y=300)
        else:
            self.putButton.place(x=400,y=300)
        self.backButton.place(x=50,y=550)

    def __destroyVillopage(self):
        """ Détruit la page de gestion de villo """
        self.listStation.destroy()
        self.takeButton.destroy()
        self.putButton.destroy()
        self.backButton.destroy()

    def __makeHistorypage(self):
        """ Dessine la page d'historique """
        self.__destroyPage()
        self.page = "history"

        # Construction widgets
        self.historyList = Listbox(self,
                                    width=80,
                                    height=30)

        self.backButton = Button(self,
                                        text="Retour",
                                        command=self.__makeManagepage)

        self.scrollbar = Scrollbar(self,orient=VERTICAL)
        self.scrollbar.config(command=self.historyList.yview)

        # On rempli la liste des déplacements
        history = self.db.getUserHistory(self.uid)
        for trips in history:
            self.historyList.insert(END, trips)

        # Placement widgets
        self.historyList.place(x=50,y=20)
        self.scrollbar.place(x=700,y=20,relheight=0.85)
        self.backButton.place(x=50,y=550)

    def __destroyHistorypage(self):
        """ Détruit la fenêtre d'historique """
        self.historyList.destroy()
        self.scrollbar.destroy()
        self.backButton.destroy()

    def __loadVilloConsult(self):
        """ Charge une liste de villo pour la consultation """
        index = self.listStation.curselection()
        stationName = self.listStation.get(index)
        villos = self.db.getVilloInStation(stationName)
        size = self.listVillo.size();
        if size > 0:
            self.listVillo.delete(0,size)
        for v in villos:
            string = str(v['VID']) + ". " + v['Modèle']
            if v['EnEtat'] == 0:
                string += " : Cassé"
            self.listVillo.insert(END, string)

    def __register(self):
        """ Gère l'enregistrement d'un utilisateur """
        # TODO: Gérer l'enregistrement
        return

    def __connect(self):
        """ Gère la connexion à un compte """
        uid = self.idEntry.get()
        passwd = self.passEntry.get()

        if self.db.checkAccount(uid,passwd):
            self.connected = True
            self.uid = uid
            self.__makeManagepage()
        else:
            print("ID ou mot de passe incorrecte")
            # TODO: Afficher une box d'erreur

    def __disconnect(self):
        """ Gère la déconnexion """
        self.connected = False
        self.__makeHomepage()

    def __takeVillo(self):
        """ Gère l'action de prendre un villo """
        index = self.listStation.curselection()
        stationName = self.listStation.get(index)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        villo = self.db.getVilloInStation(stationName)
        if len(villo) > 0:
            self.db.takeVillo(self.uid, stationName, date, villo[0]['VID'])
            #TODO: Afficher un message de validation
            print("Vous pouvez prendre le Villo n " + str(villo[0]['VID']) )
        else:
            #TODO: Afficher un message d'erreur
            print("Il n'y a plus de villo dans cette station")
        self.__makeManagepage()



    def __putVillo(self):
        """  gère l'action de remettre un villo """
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        index = self.listStation.curselection()
        stationName = self.listStation.get(index)
        # TODO: Vérifier qu'il y a de la place dans la station
        self.db.putVillo(self.uid, date, stationName)
        self.__makeManagepage()
        # TODO: Afficher une box de validation

