#!/usr/bin/python
# -*- coding:utf-8 -*-
import csv

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

			# Ajouter les villos à la base de données plutot que les afficher
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

			# Ajouter les stations à la base de donnée plutot que les afficher
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


			# Ajouter les déplacement à la base de donnée plutot que de les afficher
			print(vid,uid,depart,departTime,end,endTime)
		else:
			header = False


if ( __name__ == "__main__" ):
	# TODO: Ajout des villos
	loadVillos()
	# TODO: Ajout des stations
	loadStations()
	# TODO: Ajout des utilisateurs
	# TODO: Ajout des déplacements
	loadTrips()