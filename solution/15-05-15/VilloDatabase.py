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
