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

	def getVilloInStation(self, stationName):
		""" Renvoie la liste des villos dans une station """

		sql1 = "SELECT t1.VID, MAX(t1.DateRetour) as maxdate, t1.StationRetour \
			FROM `Trajet` t1 \
			WHERE t1.VID NOT IN (SELECT t2.VID FROM `Trajet` t2 WHERE t2.StationRetour IS NULL) \
			GROUP BY t1.VID "

		sql2 = "SELECT r.VID \
			FROM ("+sql1+") r, Station s \
			WHERE r.StationRetour = s.SID \
			AND s.Nom = \""+stationName+"\" "

		sql3 = "SELECT v.VID, v.Modèle, v.EnEtat \
			FROM ("+sql2+") res, Villo v \
			WHERE res.VID = v.VID"
		

		cursor = self.connection.cursor()
		cursor.execute(sql3)
		result = cursor.fetchall()

		vlist=list()
		for v in result:
			string = str(v['VID']) + ". " + v['Modèle']
			if v['EnEtat'] == 0:
				string += " : Cassé"
			vlist.append(string)
		return vlist

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


