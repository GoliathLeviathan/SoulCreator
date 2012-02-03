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

from PySide.QtCore import QObject, Qt, QIODevice, QByteArray, QBuffer

from src.Config import Config
from src.Error import ErrTraitType, ErrTraitCategory
from src.Debug import Debug

## Fallback to normal ElementTree, sollte lxml nicht installiert sein.
lxmlLoadad = False
try:
	from lxml import etree
	#Debug.debug("Running with lxml.etree")
	lxmlLoadad = True
except ImportError:
	try:
		# Python 2.5
		import xml.etree.cElementTree as etree
		#Debug.debug("running with cElementTree on Python 2.5+")
	except ImportError:
		try:
			# Python 2.5
			import xml.etree.ElementTree as etree
			#Debug.debug("running with ElementTree on Python 2.5+")
		except ImportError:
			print("Failed to import ElementTree from any known place")




class WriteXmlCharacter(QObject):
	"""
	@brief Schreibt die Charakterwerte in eine Datei.
	"""


	def __init__(self, character, parent=None):
		QObject.__init__(self, parent)

		self.__character = character


	def write( self, fileName ):
		"""
		Startet den Schreibvorgang.
		"""

		root = etree.Element(Config.programName, version=Config.version())

		etree.SubElement(root, "species").text = self.__character.species

		etree.SubElement(root, "era").text = self.__character.era

		## Identität
		identities = etree.SubElement(root, "identities")
		forenames = " ".join(self.__character.identity.forenames)
		etree.SubElement(identities, "identity",
			forenames=forenames,
			surname=self.__character.identity.surname,
			honorname=self.__character.identity.honorname,
			nickname=self.__character.identity.nickname,
			supername=self.__character.identity.supername,
			gender=self.__character.identity.gender,
		)
		
		## Daten
		etree.SubElement(root, "dates",
			birth=self.__character.dateBirth.toString(Config.dateFormat),
			becoming=self.__character.dateBecoming.toString(Config.dateFormat),
			game=self.__character.dateGame.toString(Config.dateFormat),
		)

		etree.SubElement(root, "virtue").text = self.__character.virtue

		etree.SubElement(root, "vice").text = self.__character.vice

		breedElement = etree.SubElement(root, "breed")
		breedElement.text = self.__character.breed
		if self.__character.species == "Changeling":
			breedElement.attrib["kith"] = self.__character.kith

		etree.SubElement(root, "faction").text = self.__character.faction

		etree.SubElement(root, "organisation").text = self.__character.organisation

		etree.SubElement(root, "party").text = self.__character.party

		etree.SubElement(root, "height").text = unicode(self.__character.height)

		etree.SubElement(root, "weight").text = unicode(self.__character.weight)

		etree.SubElement(root, "eyes").text = self.__character.eyes

		etree.SubElement(root, "hair").text = self.__character.hair

		etree.SubElement(root, "nationality").text = self.__character.nationality

		etree.SubElement(root, "description").text = self.__character.description

		etree.SubElement(root, "powerstat").text = unicode(self.__character.powerstat)

		etree.SubElement(root, "morality").text = unicode(self.__character.morality)

		## Geistesstörungen
		derangements = etree.SubElement(root, "derangements")
		for item in self.__character.derangements.items():
			if item[1]:
				etree.SubElement(derangements, "derangement", morality=unicode(item[0])).text = item[1]

		## Eigenschaften
		traits = etree.SubElement(root, "Traits")
		for item in self.__character.traits:
			traitTypeExists = False
			traitType = None
			for subitem in self.__character.traits[item]:
				traitCategoryExists = False
				traitCategory = None
				for subsubitem in self.__character.traits[item][subitem].values():
					## Eigenschaften müssen nur dann gespeichert werden, wenn ihr Wert != 0 ist und sie für die aktuell gewählte Spezies zur Verfügung stehen.
					if ( subsubitem.value != 0 and (not subsubitem.species or subsubitem.species == self.__character.species) ):
						if not traitTypeExists:
							traitType = etree.SubElement(traits, "Type", name=item)
							traitTypeExists = True
						if not traitCategoryExists:
							traitCategory = etree.SubElement(traitType, "Category", name=subitem)
							traitCategoryExists = True
						trait = etree.SubElement(traitCategory, "trait",
							name=subsubitem.name,
							value=unicode(subsubitem.value),
						)
						# Zusatztext
						if item != "Subpower" and subsubitem.custom:
							trait.attrib["customText"] =  unicode( subsubitem.customText )
						# Spezialisierungen
						if subsubitem.specialties:
							etree.SubElement(trait, "specialties").text = Config.sepChar.join( unicode(n) for n in subsubitem.specialties )

		## Gegenstände
		items = etree.SubElement(root, "Items")
		if self.__character.weapons:
			weapons = etree.SubElement(items, "Weapons")
			for category in self.__character.weapons:
				weaponCategory = etree.SubElement(weapons, "Category", name=category)
				for weapon in self.__character.weapons[category]:
					etree.SubElement(weaponCategory, "weapon").text = weapon
		if self.__character.armor:
			armor = etree.SubElement(items, "armor", dedicated=unicode(self.__character.armor["dedicated"])).text = self.__character.armor["name"]
		if self.__character.equipment or self.__character.magicalTool:
			equipment = etree.SubElement(items, "Equipment")
			for item in self.__character.equipment:
				etree.SubElement(equipment, "equipment").text = item
			if self.__character.magicalTool:
				etree.SubElement(equipment, "magicalTool").text = self.__character.magicalTool

		## Spezialseigenschaften der Spezies
		if self.__character.nimbus:
			etree.SubElement(root, "nimbus").text = self.__character.nimbus
		if self.__character.species == "Vampire" and any((x.name and x.value > 0) for x in self.__character.vinculi):
			vinculi = etree.SubElement(root, "vinculi")
			for item in self.__character.vinculi:
				if item.name and item.value > 0:
					etree.SubElement(vinculi, "vinculum", value=unicode(item.value)).text = item.name

		if self.__character.picture:
			imageData = QByteArray()
			imageBuffer = QBuffer(imageData)
			imageBuffer.open(QIODevice.WriteOnly)
			self.__character.picture.save(imageBuffer, Config.pictureFormat)	# Schreibt das Bild in ein QByteArray im angegebenen Bildformat.
			imageData = imageData.toBase64()
			etree.SubElement(root, "picture").text = unicode(imageData)

		## In die Datei schreiben.
		with open(fileName, "w") as f:
			if lxmlLoadad:
				f.write(etree.tostring(root, pretty_print=True, encoding='UTF-8', xml_declaration=True))
			else:
				f.write(etree.tostring(root, encoding='UTF-8'))
