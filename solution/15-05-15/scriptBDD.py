#!/usr/bin/python
# -*- coding:utf-8 -*-
import csv
import xml.etree.ElementTree as ET
import pymysql.cursors


def loadVillos(connection):
	""" Charge les villos du fichier villos.csv dans la base de donnée """
	reader = csv.reader(open("data/villos.csv", encoding="utf-8"),delimiter=';')
	i = 0;
	header = True
	for row in reader:
		if not header: # On ne veut pas de l'entête
			vid = int(row[0])
			date = row[1].replace("T", " ") # Mise en service
			model = row[2]
			if bool(row[3]):
				working = 1
			else:
				working = 0

			sql = "INSERT INTO `Villo` (`VID`,`DateMiseEnService`,`Modèle`,`EnEtat`) VALUES ("+str(vid)+",'"+date+"',\""+model+"\","+str(working)+")"
			connection.cursor().execute(sql)
			connection.commit()

		else:
			header = False

def loadStations(connection):
	""" Charge les stations du fichier stations.csv dans la base de donnée """
	reader = csv.reader(open("data/stations.csv", encoding="utf-8"),delimiter=";")
	header = True
	for row in reader:
		if not header:
			sid = int(row[0])
			name = row[1]
			if bool(row[2]):
				payment = 1
			else:
				payment = 0
			capacity = int(row[3])
			x = float(row[4])
			y = float(row[5])

			sql = "INSERT INTO `Station` (`SID`,`Nom`,`Longitude`,`Latitude`,`Capacité`,`BorneDePaiement`)\
			VALUES ("+str(sid)+",\""+name+"\","+str(x)+","+str(y)+","+str(capacity)+","+str(payment)+")"
			connection.cursor().execute(sql)
			connection.commit()

		else:
			header = False

def loadTrips(connection):
	""" Charge les trajets du fichier trips.csv dans la base de donnée """
	reader = csv.reader(open("data/trips.csv", encoding="utf-8"),delimiter=";")
	header = True
	for row in reader:
		if not header:
			vid = row[0]
			# Utilisateur
			uid = None
			if row[1] != "None":
				uid = int(row[1])
			# Départ
			depart = None
			if row[2] != "None":
				depart = int(row[2])

			departTime = "0000-00-00 00:00:00"
			if row[3] != "None":
				departTime = row[3].replace("T"," ")

			# Arrivée
			end = None
			if row[4] != "None":
				end = int(row[4])

			endTime = None
			if row[5] != None:
				endTime = row[5].replace("T", " ")

			if (uid == None) and (depart == None): # Si il s'agit d'un placement de vélo
				sql = "INSERT INTO `Trajet` (`VID`,`DateDépart`,`DateRetour`,`StationRetour`) \
					VALUES ("+str(vid)+", '"+departTime+"','"+endTime+"',"+str(end)+")"
			elif (end == None): # Si le vélo est toujours en déplacement
				sql = "INSERT INTO `Trajet` (`VID`,`DateDépart`,`UID`, `StationDépart`) \
					VALUES ("+str(vid)+",'"+departTime+"',"+str(uid)+","+str(depart)+")"
			else: # Déplacement normal
				sql = "INSERT INTO `Trajet` (`VID`,`DateDépart`,`UID`, `StationDépart`,`DateRetour`,`StationRetour`) \
					VALUES ("+str(vid)+",'"+departTime+"',"+str(uid)+","+str(depart)+", '"+endTime+"', "+str(end)+")"

			connection.cursor().execute(sql)
			connection.commit()

		else:
			header = False


def loadUsers(connection):
	""" Charge les utilisateurs du fichier users.xml dans la base de donnée """
	tree = ET.parse("data/users.xml")
	root = tree.getroot()

	for child in root:
		if child.tag == "subscribers":
			for subscriber in child:
				parseSubscriber(subscriber,connection)
		elif child.tag == "temporaryUsers":
			for temporary in child:
				parseTemporaryUser(temporary,connection)


def parseSubscriber(subscriber,connection):
	""" Parse un abonné dans le document xml """
	for element in subscriber:
		if element.tag == "userID":
			UID = int(element.text)
		elif element.tag == "RFID":
			RFID = int(element.text)
		elif element.tag == "lastname":
			lastname = element.text
		elif element.tag == "firstname":
			firstname = element.text
		elif element.tag == "password":
			password = int(element.text)
		elif element.tag == "phone":
			phone = element.text
		elif element.tag == "address":
			for el in element:
				if el.tag == "city":
					city = el.text
				elif el.tag == "cp":
					cp = int(el.text)
				elif el.tag == "street":
					street = el.text
				elif el.tag == "number":
					number = int(el.text)
		elif element.tag == "subscribeDate":
			subscribeDate = element.text.replace("T", " ")
		elif element.tag == "expiryDate":
			expiryDate = element.text.replace("T"," ")
		elif element.tag == "card":
			card = int(element.text)

	name = lastname + " " + firstname


	sql = "INSERT INTO `Utilisateur` (`UID`,`MotDePasse`,`CarteDeCredit`,`DateExpiration`) \
		VALUES ("+str(UID)+","+str(password)+","+str(card)+",'"+expiryDate+"')"
	connection.cursor().execute(sql)
	connection.commit()

	sql = "INSERT INTO `Abonné` (`UID`,`RFID`,`Nom`,`Rue`,`Numéro`,`CodePostal`,`Ville`,`Téléphone`,`DateInscription`) \
		VALUES ("+str(UID)+","+str(RFID)+",\""+name+"\",\""+street+"\","+str(number)+","+str(cp)+",\""+city+"\", \""+phone+"\",'"+subscribeDate+"')"
	connection.cursor().execute(sql)
	connection.commit()



def parseTemporaryUser(temporary,connection):
	""" Parse un utilisateur temporaire dans le document xml """
	for element in temporary:
		if element.tag == "userID":
			UID = int(element.text)
		if element.tag == "password":
			password = int(element.text)
		if element.tag == "expiryDate":
			expiryDate = element.text.replace("T", " ")
		if element.tag == "card":
			card = int(element.text)

	sql = "INSERT INTO `Utilisateur` (`UID`,`MotDePasse`,`CarteDeCredit`,`DateExpiration`) \
		VALUES ("+str(UID)+","+str(password)+","+str(card)+",'"+expiryDate+"')"
	connection.cursor().execute(sql)
	connection.commit()



if ( __name__ == "__main__" ):
	

	print("Connexion a MySQL ...",end="")
	# Connect to the database:
	connection = pymysql.connect(host="localhost",
								user="villodb",
								passwd="villodb",
								db="villo",
								cursorclass=pymysql.cursors.DictCursor)
	print("Fait !")
	try:
		print("Chargement des Villos")
		loadVillos(connection)
		print("Chargement des Stations")
		loadStations(connection)
		print("Chargement des utilisateurs")
		loadUsers(connection)
		print("Chargement des trajets")
		loadTrips(connection)
	finally:
		print("Fermeture de la connexion")
		connection.close()
	print("FIN !")