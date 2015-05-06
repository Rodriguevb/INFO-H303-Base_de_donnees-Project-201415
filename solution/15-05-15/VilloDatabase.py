#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql.cursors

class VilloDatabase:

	def __init__(self):
		""" Constructeur """
		self.connection = pymysql.connect(host="localhost",
										user="villodb",
										passwd="villodb",
										db="villo",
										cursorclass=pymysql.cursors.DictCursor)

	def disconnect(self):
		""" Déconnecte de la base de donnée """
		self.connection.close()

	def checkAccount(self, id, passwd):
		""" Vérifie si le compte existe et que le mot de passe est bon """
		sql = "SELECT `uid` FROM `Utilisateur` WHERE `uid`="+str(id)+" AND `MotDePasse`="+passwd+" "
		cursor = self.connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchone()
		if result != None :
			return True
		else:
			return False

	def getStationNameList(self):
		""" Renvoie la liste de nom des stations """
		sql = "SELECT `Nom` FROM `Station` ORDER BY `Nom`"
		cursor = self.connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchall()

		namelist = list()
		for station in result:
			namelist.append(station['Nom'])
		return namelist

	def isUserUsingVillo(self, uid):
		""" Vérifie si un utilisateur utilise un villo """
		sql = "SELECT `VID`,`DateDépart` FROM `Trajet` WHERE `UID`="+uid+" AND `StationRetour` IS NULL"
		cursor = self.connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchall()

		return len(result) == 1

	def getUserHistory(self, uid):
		""" Renvoie l'historique des déplacement d'un utilisateur """

		sql = "SELECT t.DateDépart, t.DateRetour, s1.Nom, s2.Nom \
			FROM `Trajet` t, `Station` s1, `Station` s2 \
			WHERE t.UID = "+str(uid)+" \
			AND t.StationDépart = s1.SID \
			AND t.StationRetour = s2.SID \
			AND t.StationRetour IS NOT NULL \
			AND t.StationDépart IS NOT NULL \
			ORDER BY t.DateDépart DESC"

		cursor = self.connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchall()

		history = list()
		for r in result:
			string = ""
			"Départ: JJ/MM/AA hh:mm:ss - Station / Arrivée: JJ/MM/AA hh:mm:ss - Station"
			string += "Départ: "+str(r['DateDépart'])+" - " + r['Nom'] +" / "
			string += "Arrivée: "+ str(r['DateRetour'])+" - " + r["s2.Nom"]
			history.append(string)
		return history

	def getVilloInStation(self, stationName,ignoreBroken=False):
		""" Renvoie la liste des villos dans une station """

		sql1 = "SELECT Trajet.VID, Trajet.DateDépart, Trajet.StationRetour FROM `Trajet`,\
				(SELECT tr.VID as vid, max(tr.DateDépart) as dr FROM `Trajet` as tr GROUP BY tr.VID) as t\
				WHERE Trajet.VID = t.vid \
				AND Trajet.DateDépart = t.dr\
				ORDER BY Trajet.VID"

		sql2 = "SELECT r.VID \
			FROM ("+sql1+") r, Station s \
			WHERE r.StationRetour = s.SID \
			AND s.Nom = \""+stationName+"\" "


		sql3 = "SELECT v.VID, v.Modèle, v.EnEtat \
			FROM ("+sql2+") res, Villo v \
			WHERE res.VID = v.VID"

		if ignoreBroken:
			sql3 += " AND v.EnEtat = 1"
		

		cursor = self.connection.cursor()
		cursor.execute(sql3)
		result = cursor.fetchall()

		return result

	def putVillo(self, uid, dateReturn, stationName):
		""" Rend un villo à la date et à la station passer en paramètre. """
		cursor = self.connection.cursor()

		sql1 = "SELECT `VID`,`DateDépart` FROM `Trajet` WHERE `UID`="+uid+" AND `StationRetour` IS NULL"
		cursor.execute(sql1)
		trip = cursor.fetchone()

		sql2 = "UPDATE `Trajet` \
				SET `StationRetour` = (SELECT `SID` FROM `Station` WHERE `Nom`=\""+stationName+"\" ), \
				`DateRetour` = '"+dateReturn+"' \
				WHERE `DateDépart` = '"+str(trip['DateDépart'])+"' \
				AND `VID` = "+str(trip['VID'])+" "

		cursor.execute(sql2)
		self.connection.commit()

	def takeVillo(self, uid, stationName, dateStart, vid):
		""" Donner un villo. Provient de la station à la date pour l'utilisateur passer en paramètre. """
		cursor = self.connection.cursor()

		sql1= "SELECT `SID` FROM Station WHERE `Nom`=\""+stationName+"\" "

		cursor.execute(sql1)

		station = cursor.fetchone()

		sql2 = "INSERT INTO `Trajet` (`VID`,`DateDépart`,`UID`, `StationDépart`) \
					VALUES ("+str(vid)+",'"+str(dateStart)+"',"+str(uid)+","+str(station['SID'])+")"

		cursor.execute(sql2)
		self.connection.commit()

	def getVilloIDFromUser(self, uid):
		""" Renvoie l'id du Villo qu'utilise un utilisateur. """
		sql = "SELECT `VID` FROM `Trajet` WHERE `UID`="+uid+" AND `StationRetour` IS NULL"
		cursor = self.connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchone()

		return result['VID']

	def signalProblem(self, vid):
		""" Signal un problème sur le villo passé en paramètre """
		sql = "UPDATE `Villo` \
				SET `EnEtat` = 0 \
				WHERE `VID`= "+str(vid)+" "
		cursor = self.connection.cursor()
		cursor.execute(sql)
		self.connection.commit()

	def getNewUserID(self):
		""" Récupère un nouvel id Utilisateur """

		sql = "SELECT max(`UID`) as id FROM `Utilisateur`"
		cursor = self.connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchone()
		
		return result['id']+1

	def isRFIDfree(self,rfid):
		""" Vérifie si un RFID est libre """

		sql = "SELECT * FROM `Abonné` WHERE `RFID`="+str(rfid)+" "
		cursor = self.connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchall()

		return len(result) == 0

	def createSubscriber(self,uid,rfid,passwd,name,phone,city,cp,street,number,card,dateSub,dateExp):
		""" Crée un utilisateur abonné """
		sql = "INSERT INTO `Utilisateur` (`UID`,`MotDePasse`,`CarteDeCredit`,`DateExpiration`) \
		VALUES ("+uid+","+passwd+","+card+",'"+dateExp+"')"
		self.connection.cursor().execute(sql)
		self.connection.commit()

		sql = "INSERT INTO `Abonné` (`UID`,`RFID`,`Nom`,`Rue`,`Numéro`,`CodePostal`,`Ville`,`Téléphone`,`DateInscription`) \
		VALUES ("+uid+","+rfid+",\""+name+"\",\""+street+"\","+number+","+cp+",\""+city+"\", \""+phone+"\",'"+dateSub+"')"
		self.connection.cursor().execute(sql)
		self.connection.commit()

	def getUserExpiryDate(self, uid):
		""" Renvoie la date d'expiration d'un utilisateur """
		sql = "SELECT `DateExpiration` FROM `Utilisateur` WHERE `UID` = "+str(uid)+" "
		cursor = self.connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchone()
		if result != None:
			return result['DateExpiration']
		else:
			return None


