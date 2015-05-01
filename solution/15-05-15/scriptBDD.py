#!/usr/bin/python
# -*- coding:utf-8 -*-
import csv

def loadVillos():
	""" Charge les villos du fichier villos.csv dans la base de donnée """
	reader = csv.reader(open("data/villos.csv", encoding="utf-8"),delimiter=';')
	i = 0;
	for row in reader:
		if i != 0: # On ne veut pas de l'entête
			vid = int(row[0])
			date = row[1].replace("T", " ") # Mise en service
			model = row[2]
			working = bool(row[3])

			# Ajouter les villos à la base de données
			print(vid,date,model,working)

		i+=1


if ( __name__ == "__main__" ):
	# TODO: Ajout des villos
	loadVillos()
	# TODO: Ajout des stations
	# TODO: Ajout des utilisateurs
	# TODO: Ajout des déplacements