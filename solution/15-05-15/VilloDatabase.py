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
		sql = "SELECT `MotDePasse` FROM `Utilisateur` WHERE `uid`="+str(id)+""
		cursor = self.connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchone()
		if (result != None) and (passwd.isdigit()):
			return result['MotDePasse'] == int(passwd)
		else:
			return False
