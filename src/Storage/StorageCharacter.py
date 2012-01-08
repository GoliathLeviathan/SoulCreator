# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) Victor von Rhein, 2011, 2012

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

from PySide.QtCore import QObject, Signal, Slot

from src.Config import Config
from src.Datatypes.Trait import Trait
from src.Datatypes.Identity import Identity
from src.Error import ErrListLength
from src.Debug import Debug




class StorageCharacter(QObject):
	"""
	@brief In dieser Klasse werden sämtliche Daten des gerade geöffneten Charakters gespeichert.

	Wird ein Wert durch das Programm geändert, muß der Wert tatsächlich in dieser Klasse verändert werden. Denn der Inhalt dieser Klasse wird beim Speichern in eine Datei geschrieben und beim Laden wird diese Klasse aufgefüllt. Die Anzeige nimmt all ihre Daten aus dieser Klasse.

	Außerdem bietet diese Klasse angenehme Zugriffsfunktionen aus den Informationen, welche zum Programmstart aus den Template-Dateien geladen werden.
	"""


	ageChanged = Signal(int)
	speciesChanged = Signal(str)
	virtueChanged = Signal(str)
	viceChanged = Signal(str)
	breedChanged = Signal(str)
	factionChanged = Signal(str)
	powerstatChanged = Signal(int)
	moralityChanged = Signal(int)
	armorChanged = Signal(object)
	#traitChanged = Signal(object)
	#traitsChanged = Signal(object)
	eraChanged = Signal(str)


	# Eine Liste sämtlicher verfügbaren Eigenschaften.
	#
	# {
	# 	Typ1: {
	# 		Kategorie1: {
	# 			Name1: { "bla": blub, ... }
	# 			Name2: { "bla": blub, ... }
	# 			Name3: { "bla": blub, ... }
	# 			...
	# 		},
	# 		Kategorie2: {
	# 			Name1: { "bla": blub, ... }
	# 			...
	# 		},
	# 		...
	# 	},
	# 	...
	# }
	__traits = {}


	def __init__(self, template, parent=None):
		QObject.__init__(self, parent)

		self.__storage = template

		self.__modified = False
		self.__age = 0
		self.__species = ""
		self.__virtue = ""
		self.__vice = ""
		self.__breed = ""
		self.__faction = ""
		self.__powerstat = 0
		self.__morality = 0
		self.__armor = [0, 0]
		self.__era = ""

		self.__identity = Identity()
		self.__identities = [self.__identity]

		self.__derangements = []

		# Die Eigenschaften in den Charakter laden.
		self.__traits = {}
		# Eigenscahften setzen.
		for typ in Config.typs:
			self.__traits.setdefault(typ, {})
			for item in template.traits[typ]:
				self.__traits[typ].setdefault(item, {})
				for subitem in template.traits[typ][item].items():
					#Debug.debug(subitem)
					val = 2
					# Eigenschaften, die Zusaztest erhalten können (bspw. Language), werden mehrfach an die Liste angefügt.
					loop = 1
					custom = False
					customText = None
					if subitem[1]["custom"]:
						loop = Config.traitMultipleMax
						custom = True

					for i in xrange(loop):
						trait = Trait(self, subitem[0], val)
						trait.age = subitem[1]["age"]
						trait.era = subitem[1]["era"]
						trait.species = subitem[1]["species"]
						trait.custom = custom
						trait.customText = customText
						if "prerequisite" in subitem[1]:
							trait.hasPrerequisites = True
							trait.prerequisitesText = subitem[1]["prerequisite"]
						self.__traits[typ][item].setdefault(subitem[0], trait)

						# Wenn sich eine Eigenschaft ändert, gilt der Charakter als modifiziert.
						trait.traitChanged.connect(self.setModified)

					

		# Sobald irgendein Aspekt des Charakters verändert wird, muß festgelegt werden, daß sich der Charkater seit dem letzten Speichern verändert hat.
		# Es ist Aufgabe der Speicher-Funktion, dafür zu sorgen, daß beim Speichern diese Inforamtion wieder zurückgesetzt wird.
		self.__identity.identityChanged.connect(self.setModified)
		self.speciesChanged.connect(self.setModified)
	#connect( self, SIGNAL( traitChanged( cv_Trait* ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( derangementsChanged() ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( virtueChanged( QString ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( viceChanged( QString ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( breedChanged( QString ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( factionChanged( QString ) ), self, SLOT( setModified() ) );
		self.powerstatChanged.connect(self.setModified)
	#connect( self, SIGNAL( moralityChanged( int ) ), self, SLOT( setModified() ) );
	#connect( self, SIGNAL( armorChanged( int, int ) ), self, SLOT( setModified() ) );

	#connect (self, SIGNAL(realIdentityChanged(cv_Identity)), self, SLOT(emitNameChanged(cv_Identity)));


	def __getEra(self):
		"""
		Gibt die Ära aus, in welcher der Charakter zuhause ist.
		"""

		return self.__era

	def __setEra( self, era ):
		"""
		Legt die Ära fest, in welcher der Charakter zuhause ist.
		"""

		if ( self.__era != era ):
			self.__era = era
			#Debug.debug("Ära verändert zu {}".format(era) )
			self.eraChanged.emit( era )

	era = property(__getEra, __setEra)


	def __getAge(self):
		"""
		Gibt das Alter des Charakters aus.
		"""

		return self.__age

	def __setAge( self, age ):
		"""
		Legt das Alter des Charakters fest.
		"""

		if ( self.__age != age ):
			self.__age = age
			#Debug.debug("Alter verändert zu {}".format(age) )
			self.ageChanged.emit( age )

	age = property(__getAge, __setAge)


	def __getSpecies(self):
		"""
		Gibt die Spezies des Charakters aus.
		"""
		
		return self.__species

	def __setSpecies( self, species ):
		"""
		Legt die Spezies des Charakters fest.
		"""
		
		if ( self.__species != species ):
			self.__species = species
			#Debug.debug("Spezies in Speicher verändert zu {}!".format(species))
			self.speciesChanged.emit( species )

	species = property(__getSpecies, __setSpecies)


	def __getIdentities(self):
		"""
		Gibt eine Liste aller Identitäten des Charkaters aus. Die Identität an Indexposition 0 ist die echte Identität.
		"""
		
		return self.__identities

	identities = property(__getIdentities)


	#def insertIdentity( self, index, identity ):
		#"""
		#Fügt eine neue Identität an der angegebenen Stelle ein.
		#"""
		
		#self.__identities.insert( index, identity )
		#self.identityChanged.emit( identity )

	#def addIdentity( self, identity ):
		#"""
		#Hängt eine neue Identität an die Liste aller Identitäten des Charkaters an.
		#"""
		
		#self.__identities.append( identity )
		#self.identityChanged.emit( identity )

	#def setRealIdentity( self, identity ):
		#"""
		#Legt die \emph{echte} Identität des Charakters fest. Diese Identität hat immer Index 0 in der \ref self.__identities -Liste
		
		#\todo Momentan ist dies die einzige identität, die von diesem programm genutzt wird.
		#"""

		#if self.__identities[0] != identity:
			#self.__identities[0] = identity
			#self.identityChanged.emit( identity )
			#self.realIdentityChanged.emit( identity )


	def __getTraits(self):
		return self.__traits

	#def __setTraits(self, traits):
		#if self.__traits != traits:
			#self.__traits = traits
			#self.traitsChanged.emit(traits)

	traits = property(__getTraits)



	#def addTrait( self, typ, category, trait ):
		#"""
		#Fügt dem Speicher eine neue Eigenschaft hinzu.
		 
		#\note Doppelte Eigenschaften werden mit dem neuen Wert überschrieben.
		 
		#\todo Eigenschaften mit Zusatztext werden nur gespeichert, wenn dieser Text auch vorhanden ist.
		#"""

		#if typ not in self.__traits:
			#self.__traits.setdefault(typ,{})

		#if category not in self.__traits[typ]:
			#self.__traits[typ].setdefault(category,[])

		#self.__traits[typ][category].append(trait)

		#return self.__traits[typ][category][:-1]


	#def modifyTrait( self, typ, category, trait ):
		#"""
		#Ändert eine Eigenschaft im Speicher.
		#"""

		#for item in self.__traits[typ][category]:
			#if trait["name"] == item["name"]:
				#if item["value"] != trait["value"]:
					#item["value"] = trait["value"]
					#self.traitChanged.emit(item)
				## Es fehlen noch "customText" und "Details"
				#break


#QList< cv_Derangement >* StorageCharacter::derangements() const {
	#return &v_derangements;
#}

#QList< cv_Derangement* > StorageCharacter::derangements( cv_AbstractTrait::Category category ) const {
	#QList< cv_Derangement* > list;

	#for ( int i = 0; i < v_derangements.count(); ++i ) {
		#if ( v_derangements.at( i ).category() == category ) {
			#list.append( &v_derangements[i] );
		#}
	#}

	#return list;
#}

#void StorageCharacter::addDerangement( cv_Derangement derang ) {
	#if ( !derang.name().isEmpty() && !v_derangements.contains( derang ) ) {
#// 		qDebug() << Q_FUNC_INFO << derang.name << derang.morality;
		#v_derangements.append( derang );

		#emit derangementsChanged();
	#}
#}

#void StorageCharacter::removeDerangement( cv_Derangement derang ) {
	#if ( v_derangements.contains( derang ) ) {
		#v_derangements.removeAll( derang );
		#emit derangementsChanged();
	#}
#}


	def __getVirtue(self):
		"""
		Tugend des Charakters
		"""

		return self.__virtue

	def __setVirtue( self, virtue ):
		"""
		Verändert die Tugend.

		Bei einer Veränderung wird das Signal virtueChanged() ausgesandt.
		"""

		if ( self.__virtue != virtue ):
			self.__virtue = virtue
			self.virtueChanged.emit( virtue )

	virtue = property(__getVirtue, __setVirtue)


	def __getVice(self):
		"""
		Laster des Charakters
		"""

		return self.__vice

	def __setVice( self, vice ):
		"""
		Verändert das Laster.

		Bei einer Veränderung wird das Signal viceChanged() ausgesandt.
		"""

		if ( self.__vice != vice ):
			self.__vice = vice
			self.viceChanged.emit( vice )

	vice = property(__getVice, __setVice)


	def __getBreed(self ):
		"""
		Brut (Seeming, Path, Clan, Auspice) des Charakters.
		"""

		return self.__breed

	def __setBreed( self, breed ):
		"""
		Verändert die Brut.

		Bei einer Veränderung wird das Signal breedChanged() ausgesandt.
		"""

		if ( self.__breed != breed ):
			self.__breed = breed
			self.breedChanged.emit( breed)

	breed = property(__getBreed, __setBreed)


	def __getFaction(self):
		"""
		Fraktion (Court, order, Covenant, Tribe) des Charakters.
		"""

		return self.__faction

	def __setFaction( self, faction ):
		"""
		Verändert die Fraktion.

		Bei einer Veränderung wird das Signal factionChanged() ausgesandt.
		"""

		if ( self.__faction != faction ):
			self.__faction = faction
			self.factionChanged.emit( faction )

	faction = property(__getFaction, __setFaction)


	def __getPowerstat(self):
		"""
		Gibt den Wert des Super-Attributs aus.
		"""

		return self.__powerstat

	def setPowerstat( self, value ):
		"""
		Verändert den Wert des Super-Attributs.
		
		Bei einer Veränderung wird das Signal powerstatChanged() ausgesandt.
		"""

		if ( self.__powerstat != value ):
			self.__powerstat = value
			self.powerstatChanged.emit( value )

	powerstat = property(__getPowerstat, setPowerstat)


	def __getMorality(self):
		"""
		Gibt den Wert der Moral aus.
		"""

		return self.__morality

	def setMorality( self, value ):
		"""
		Verändert den Wert der Moral.
		
		Bei einer Veränderung wird das Signal moralityChanged() ausgesandt.
		"""

		if ( self.__morality != value ):
			self.__morality = value
			#Debug.debug("Moral verändert auf {}".format(value))
			self.moralityChanged.emit( value )

	morality = property(__getMorality, setMorality)


	def __getArmor(self):
		"""
		Gibt den Wert der getragenen Rüstung aus. Zurückgegeben wird eine Liste mit zwei EInträgen.
		
		Die erste Zahl stellt den Rüstungswert gegen alle Angriffe mit Ausnahme von Schußwaffen und Bögen dar.

		Die zweite Zahl stellt dagegen den Rüstungswert gegen Schußwaffen und Bögen dar.
		"""

		return self.__armor

	def __setArmor( self, armor ):
		"""
		Verändert den Wert der Rüstung.

		Es muß eine Liste mit zwei Elementen übergeben werden.
		
		Bei einer Veränderung wird das Signal armorChanged() ausgesandt.
		"""

		if len(armor) == 2:
			if self.__armor != armor:
				self.__armor = armor
				self.armorChanged.emit( self.__armor )
		else:
			raise ErrListLength(len(self.__armor), len(armor))

	armor = property(__getArmor, __setArmor)


	def resetCharacter(self):
		# Zeitalter festlegen.
		self.era = Config.eras[0]

		# Standardalter festlegen.
		self.age = Config.initialAge

		# Löschen aller Identitäten.
		self.__identity.reset()

		# Standardspezies ist der Mensch.
		self.species = Config.initialSpecies

		#Debug.debug(self.__storage.virtues[0])
		#Debug.debug(self.__storage.virtues[0]["name"])
		self.virtue = self.__storage.virtues[0]["name"]
		self.vice = self.__storage.vices[0]["name"]

		# Menschen haben eine Leere liste, also kann ich auch die Indizes nicht ändern.
		#// setBreed(storage.breedNames(species()).at(0));
		#// setFaction(storage.breedNames(species()).at(0));

		# Attribute und andere Eigenschaften auf Anfangswerte setzen.
		for item in self.__traits:
			val = 0
			if item == "Attribute":
				val = 1
			for subitem in self.__traits[item]:
				for subsubitem in self.__traits[item][subitem].values():
					subsubitem.value = val
					subsubitem.customText = ""
					subsubitem.specialties = []

		self.morality = Config.moralityTraitDefaultValue

		# Übernatürliche Eigenschaft festlegen.
		self.powerstat = Config.powerstatDefaultValue


	def isModifed(self):
		return self.__modified

	def setModified( self, sw=True ):
		if ( self.__modified != sw ):
			self.__modified = sw


	def checkPrerequisites(self, trait):
		"""
		Diese Funktion überprüft, ob die Voraussetzungen der Eigenscahft "trait" erfüllt sind ode rnicht.
		"""

		if type(trait) != Trait:
			Debug.debug("Error!")
		else:
			if trait.hasPrerequisites:
				traitPrerequisites = trait.prerequisitesText[0]
				for item in Config.typs:
					categories = self.__storage.categories(item)
					for subitem in categories:
						for subsubitem in self.traits[item][subitem].values():
							# Überprüfen ob die Eigenschaft im Anforderungstext des Merits vorkommt.
							if subsubitem.name in traitPrerequisites:
								# Vor dem Fertigkeitsnamen darf kein anderes Wort außer "and", "or" und "(" stehen.
								idxA = traitPrerequisites.index(subsubitem.name)
								strBefore = traitPrerequisites[:idxA]
								strBefore = strBefore.rstrip()
								strBeforeList = strBefore.split(" ")
								if not strBeforeList[-1] or strBeforeList[-1] == u"and" or strBeforeList[-1] == u"or" or strBeforeList[-1] == u"(":
									# Wenn Spezialisierungen vorausgesetzt werden.
									if "." in traitPrerequisites and "{}.".format(subsubitem.name) in traitPrerequisites:
										idx =[0,0]
										idx[0] = traitPrerequisites.index("{}.".format(subsubitem.name))
										idx[1] = traitPrerequisites.index(" ", idx[0])
										specialty = traitPrerequisites[idx[0]:idx[1]].replace("{}.".format(subsubitem.name), "")
										if specialty in subsubitem.specialties:
											traitPrerequisites = traitPrerequisites.replace(".{}".format(specialty), "")
										else:
											traitPrerequisites = traitPrerequisites.replace("{}.{}".format(subsubitem.name, specialty), "0")
									traitPrerequisites = traitPrerequisites.replace(subsubitem.name, unicode(subsubitem.value))
				# Es kann auch die Supereigenschaft als Voraussetzung vorkommen.
				if Config.powerstatIdentifier in traitPrerequisites:
					traitPrerequisites = traitPrerequisites.replace(Config.powerstatIdentifier, unicode(self.__powerstat))

				# Die Voraussetzungen sollten jetzt nurnoch aus Zahlen und logischen Operatoren bestehen.
				try:
					result = eval(traitPrerequisites)
					#print("Eigenschaft {} ({} = {})".format(trait.name, traitPrerequisites, result))
				except (NameError, SyntaxError) as e:
					Debug.debug("Error: {}".format(traitPrerequisites))
					result = False

				trait.setAvailable(result)
