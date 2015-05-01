#!/usr/bin/python
# -*- coding:utf-8 -*-
import csv
import xml.etree.ElementTree as ET

def loadVillos():
	""" Charge les villos du fichier villos.csv dans la base de donnée """
	reader = csv.reader(open("data/villos.csv", encoding="utf-8"),delimiter=';')
	i = 0;
	header = True
	for row in reader:
		if not header: # On ne veut pas de l'entête
			vid = int(row[0])
			date = row[1].replace("T", " ") # Mise en service
			model = row[2]
			working = bool(row[3])

			# TODO: Ajouter les villos à la base de données plutot que les afficher
			print(vid,date,model,working)
		else:
			header = False

def loadStations():
	""" Charge les stations du fichier stations.csv dans la base de donnée """
	reader = csv.reader(open("data/stations.csv", encoding="utf-8"),delimiter=";")
	header = True
	for row in reader:
		if not header:
			sid = int(row[0])
			name = row[1]
			payment = bool(row[2])
			capacity = int(row[3])
			x = float(row[4])
			y = float(row[5])

			# TODO: Ajouter les stations à la base de donnée plutot que les afficher
			print(sid,name,payment,capacity,x,y)

		else:
			header = False

def loadTrips():
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


			# TODO: Ajouter les déplacement à la base de donnée plutot que de les afficher
			print(vid,uid,depart,departTime,end,endTime)
		else:
			header = False


def loadUsers():
	""" Charge les utilisateurs du fichier users.xml dans la base de donnée """
	tree = ET.parse("data/users.xml")
	root = tree.getroot()

	for child in root:
		if child.tag == "subscribers":
			for subscriber in child:
				parseSubscriber(subscriber)
		elif child.tag == "temporaryUsers":
			for temporary in child:
				parseTemporaryUser(temporary)


def parseSubscriber(subscriber):
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

	# TODO: Ajouter les abonnés à la base de donnée plutot que de les afficher
	print(UID,RFID, name, password, phone, city, cp, street, number, subscribeDate,expiryDate,card)

def parseTemporaryUser(temporary):
	""" Parse un utilisateur temporaire dans le document xml """
	for element in temporary:
		if element.tag == "userID":
			UID = int(element.text)
		if element.tag == "password":
			password = int(element.text)
		if element.tag == "expiryDate":
			expiry = element.text.replace("T", " ")
		if element.tag == "card":
			card = int(element.text)

	# TODO: Ajouter les utilisateurs temporaires à la base de donnée plutot que les afficher
	print(UID,password,expiry,card)



if ( __name__ == "__main__" ):
	# TODO: Ajout des villos
	loadVillos()
	# TODO: Ajout des stations
	loadStations()
	# TODO: Ajout des utilisateurs
	loadUsers()
	# TODO: Ajout des déplacements
	loadTrips()