CREATE TABLE Bruker (
	BrukerID	INTEGER NOT NULL,
	Fornavn		VARCHAR(30) NOT NULL,
	Etternavn	VARCHAR(30) NOT NULL,
	Passord		VARCHAR(30) NOT NULL,
	Epostadresse	VARCHAR(64) UNIQUE NOT NULL,
	CONSTRAINT Bruker_PK PRIMARY KEY (BrukerID));

CREATE TABLE Kaffesmaking (
	BrukerID	INTEGER NOT NULL DEFAULT 0,
	SekvensNr	INTEGER NOT NULL,
	AntallPoeng	INTEGER CHECK(AntallPoeng BETWEEN 0 AND 10) NOT NULL,
	Smaksnotater	VARCHAR(300),
	Dato	DATE NOT NULL,
	BrentKaffeNavn	VARCHAR(30) NOT NULL DEFAULT '0',
	BrenneriID	INTEGER NOT NULL DEFAULT 0,
	PartiID		INTEGER NOT NULL DEFAULT 0,
	CONSTRAINT Kaffesmaking_PK PRIMARY KEY (BrukerID, SekvensNr),
	CONSTRAINT Kaffesmaking_FK1 FOREIGN KEY (BrukerID) REFERENCES Bruker(BrukerID)
		ON UPDATE CASCADE
		ON DELETE SET DEFAULT,
	CONSTRAINT Kaffesmaking_FK2 FOREIGN KEY (PartiID, BrenneriID, BrentKaffeNavn) REFERENCES BrentKaffe(PartiID, BrenneriID, BrentKaffeNavn)
		ON UPDATE CASCADE
		ON DELETE SET DEFAULT);

CREATE TABLE BrentKaffe (
	BrentKaffeNavn VARCHAR(30) NOT NULL,
	Brenningsgrad INTEGER CHECK(Brenningsgrad BETWEEN 1 AND 3) NOT NULL, /* 1 = lys, 2 = middels, 3 = mork */
	BrenneDato	DATE NOT NULL,
	Beskrivelse	VARCHAR(300),
	KiloprisKr INTEGER CHECK(KiloprisKr > 0) NOT NULL,
	BrenneriID	INTEGER NOT NULL DEFAULT 0,
	PartiID	INTEGER NOT NULL DEFAULT 0,
	CONSTRAINT BrentKaffe_PK PRIMARY KEY (BrenneriID, PartiID, BrentKaffeNavn),
	CONSTRAINT BrentKaffe_FK1 FOREIGN KEY (BrenneriID) REFERENCES Brenneri(BrenneriID)
		ON UPDATE CASCADE
		ON DELETE SET DEFAULT,
	CONSTRAINT BrentKaffe_FK2 FOREIGN KEY (PartiID) REFERENCES Parti(PartiID)
		ON UPDATE CASCADE
		ON DELETE SET DEFAULT);

CREATE TABLE Brenneri (
	BrenneriID INTEGER NOT NULL,
	BrenneriNavn VARCHAR(30) NOT NULL,
	CONSTRAINT Brenneri_PK PRIMARY KEY (BrenneriID));

CREATE TABLE Parti (
	PartiID	INTEGER NOT NULL,
	InnhostingsAr YEAR NOT NULL,
	PrisTilGardUSD INTEGER CHECK(PrisTilGardUSD > 0) NOT NULL,
	GardID	INTEGER NOT NULL,
	ForedlingNavn INTEGER NOT NULL,
	CONSTRAINT Parti_PK PRIMARY KEY (PartiID),
	CONSTRAINT Parti_FK1 FOREIGN KEY (GardID) REFERENCES Gard(GardID)
		ON UPDATE CASCADE
		ON DELETE SET DEFAULT,
	CONSTRAINT Parti_FK2 FOREIGN KEY (ForedlingNavn) REFERENCES Foredlingsmetode(Navn)
		ON UPDATE CASCADE
		ON DELETE SET DEFAULT);

CREATE TABLE Gard (
	GardID	INTEGER NOT NULL,
	Gardsnavn VARCHAR(30) NOT NULL,
	Moh	INTEGER CHECK(Moh > 0) NOT NULL,
	Region VARCHAR(30) NOT NULL,
	Land VARCHAR(30) NOT NULL,
	CONSTRAINT Gard_PK PRIMARY KEY (GardID));

CREATE TABLE Foredlingsmetode (
	Navn VARCHAR(30) NOT NULL,
	Metode VARCHAR(30) NOT NULL,
	Beskrivelse VARCHAR(300) NOT NULL,
	CONSTRAINT Foredlingsmetode_PK PRIMARY KEY (Navn));

CREATE TABLE Kaffebonner (
	ArtID INTEGER CHECK(ArtID BETWEEN 1 AND 3) NOT NULL, /* CoffeaArabica = 1, CoffeaRobusta = 2, CoffeaLiberica = 3 */
	CONSTRAINT Kaffebonner_PK PRIMARY KEY (ArtID));