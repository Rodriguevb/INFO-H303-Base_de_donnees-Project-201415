CREATE TABLE `Utilisateur` (
	`UID` mediumint unsigned NOT NULL,
	`MotDePasse` smallint(4) unsigned zerofill NOT NULL,
	`CarteDeCredit` bigint(16) unsigned zerofill NOT NULL,
	`DateExpiration` datetime NOT NULL,
	PRIMARY KEY (`UID`)
);

CREATE TABLE `Villo` (
	`VID` smallint unsigned NOT NULL,
	`DateMiseEnService` datetime NOT NULL,
	`Modèle` varchar(12) NOT NULL,
	`EnEtat` tinyint(1) NOT NULL,
	PRIMARY KEY (`VID`)
);

CREATE TABLE `Abonné` (
	`UID` mediumint unsigned NOT NULL,
	`RFID` char(20) NOT NULL,
	`Nom` varchar(50) NOT NULL,
	`Rue` varchar(100) NOT NULL,
	`Numéro` smallint unsigned NOT NULL,
	`CodePostal` smallint(4) unsigned NOT NULL,
	`Ville` varchar(50) NOT NULL,
	`Téléphone` varchar(10) NOT NULL,
	`DateInscription` datetime NOT NULL,
	PRIMARY KEY (`RFID`),
	FOREIGN KEY (`UID`) REFERENCES Utilisateur(`UID`)
);

CREATE TABLE `Station` (
	`SID` smallint unsigned NOT NULL,
	`Nom` varchar(50) NOT NULL,
	`Longitude` float NOT NULL,
	`Latitude` float NOT NULL,
	`Capacité` tinyint unsigned NOT NULL,
	`BorneDePaiement` tinyint(1) NOT NULL,
	PRIMARY KEY (`SID`,`Longitude`,`Latitude`)
);

CREATE TABLE `Trajet` (
	`VID` smallint unsigned NOT NULL,
	`DateDépart` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
	`UID` mediumint unsigned DEFAULT NULL,
	`StationDépart` smallint unsigned DEFAULT NULL,
	`DateRetour` datetime DEFAULT NULL,
	`StationRetour` smallint unsigned DEFAULT NULL,
	PRIMARY KEY (`VID`,`DateDépart`),
	FOREIGN KEY (`VID`) REFERENCES Villo(`VID`),
	FOREIGN KEY (`UID`) REFERENCES Utilisateur(`UID`),
	FOREIGN KEY (`StationDépart`) REFERENCES Station(`SID`),
	FOREIGN KEY (`StationRetour`) REFERENCES Station(`SID`)
);