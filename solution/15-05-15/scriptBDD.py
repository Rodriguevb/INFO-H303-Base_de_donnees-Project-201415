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


if ( __name__ == "__main__" ):
	# TODO: Ajout des villos
	loadVillos()
	# TODO: Ajout des stations
	loadStations()
	# TODO: Ajout des utilisateurs
	# TODO: Ajout des déplacements