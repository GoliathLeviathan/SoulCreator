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

import os
import ast
import StringIO

from PySide.QtCore import QObject, QDir, QFile, QIODevice, QResource, Signal

from src.Config import Config
from src.GlobalState import GlobalState
from src import Error
from src.Tools import ListTools
from src.Error import ErrXmlParsing, ErrXmlOldVersion, ErrFileNotOpened
from src.IO.ReadXml import ReadXml
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




class ReadXmlTemplate(QObject, ReadXml):
	"""
	@brief Liest die Eigenschaften aus den beigefügten xml-Dateien.

	Diese Klasse dient dazu einen möglichst simplen Zugriff auf die Eigenschaften der WoD-Charaktere zu bieten. Dazu werden die Eigenschaften und all ihre Zusatzinformationen aus den xml-Dateien gelesen und in Listen gespeichert.
	"""


	exceptionRaised = Signal(str, bool)


	def __init__(self, template, parent=None):
		QObject.__init__(self, parent)
		ReadXml.__init__(self)

		self.__storage = template

		## Die Template-Dateien alle für das Laden vorbereiten.
		self.__templateFiles = []
		pathToTemplates = ":/template/xml"
		templateDir = QDir(pathToTemplates)
		for templateFile in templateDir.entryList():
			self.__templateFiles.append("{}/{}".format(pathToTemplates, templateFile))


	def read(self):
		"""
		Diese Methode startet den Lesevorgang.

		Es wird kontrolliert, ob es sich um eine Zuässige Template-Datei für dieses Programm handelt

		\exception ErrXmlTooOldVersion Die XML-Datei hat die falsche Version.

		\exception ErrXmlOldVersion Die XML-Datei hat die falsche Version.

		\exception ErrXmlParsing Beim Parsen der XML-Datei ist ein Fehler aufgetreten.
		"""

		for item in self.__templateFiles:
			#Debug.debug("Lese aus Datei: {}".format(item))
			qrcFile = QFile(item)
			if not qrcFile.open(QIODevice.ReadOnly):
				raise ErrFileNotOpened(item, qrcFile.errorString())
			fileContent = ""
			while not qrcFile.atEnd():
				fileContent += qrcFile.readLine()
			qrcFile.close()
			fileLike = StringIO.StringIO(str(fileContent))
			xmlContent = etree.parse(fileLike)
			xmlRootElement = xmlContent.getroot()

			versionSource = xmlRootElement.attrib["version"]
			#Debug.debug(versionSource)

			try:
				self.checkXmlVersion( xmlRootElement.tag, versionSource )
			except ErrXmlOldVersion as e:
				messageText = self.tr("While opening the template file {}, the following problem arised:\n{} {}\nIt appears, that the file will be importable, so the process will be continued but errors may occur.".format(qrcFile.fileName(), e.message, e.description))
				self.exceptionRaised.emit(messageText, e.critical)

			species = self.readSpecies(xmlContent)
			self.readTemplate(xmlContent, species)


	def readSpecies(self, tree):
		"""
		Einlesen der Spezies, für welche die Eigenschaften in der gerade eingelsenen Datei gelten.
		"""

		traitsRoot = tree.find("Template")
		species = ""
		if "species" in traitsRoot.attrib:
			species = traitsRoot.attrib["species"]

		return species


	def readTemplate(self, tree, species):
		"""
		Einlesen aller verfügbarer Eigenschaften.
		"""

		self.readSpeciesData(tree.find("Template/Traits"), species)
		self.readCharacteristics(tree.find("Template/Traits/Virtue"))
		self.readCharacteristics(tree.find("Template/Traits/Vice"))
		self.readTraits(tree.find("Template/Traits/Attribute"), species)
		self.readTraits(tree.find("Template/Traits/Skill"), species)
		self.readTraits(tree.find("Template/Traits/Merit"), species)
		self.readTraits(tree.find("Template/Traits/Flaw"), species)
		self.readTraits(tree.find("Template/Traits/Power"), species)
		self.readSubPowers(tree.find("Template/Traits/Subpower"), species)
		self.readCreationPoints(tree.find("Template/Creation"), species)
		self.readGroups(tree.find("Template/Group/Breed"), species)
		self.readGroups(tree.find("Template/Group/Faction"), species)
		self.readGroups(tree.find("Template/Group/Organisation"), species)
		self.readGroups(tree.find("Template/Group/Party"), species)
		self.readPowerstat(tree.find("Template/Traits/Powerstat"), species)
		self.readDerangements(tree.find("Template/Traits/Derangement"), species)
		self.readWeapons(tree.findall("Template/Items/Weapons"))
		self.readArmor(tree.findall("Template/Items/Armor"))
		self.readEquipment(tree.findall("Template/Items/Equipment"))


	def readSpeciesData(self, root, species):
		"""
		Einlesen aller Spezies-abhängigen Parameter.
		"""

		speciesData = {
			"morale": self.getElementAttribute(root, "morale"),
			"powerstat": self.getElementAttribute(root, "powerstat"),
			"fuel": self.getElementAttribute(root, "fuel"),
		}

		self.__storage.appendSpecies( species, speciesData )


	def readCharacteristics(self, root):
		"""
		Einlesen aller Tugenden.
		"""

		characteristics = self.__readTraitData(root)

		for item in characteristics:
			self.__storage.appendCharacteristic(root.tag, item)


	def readTraits( self, root, species ):
		"""
		Lese die Eigenschaften aus den Template-Dateien.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		if root is not None:
			if root.tag == "Power":
				self.__storage.setPowerName(species, self.getElementAttribute(root, "name"))
			for category in root.getiterator("Category"):
				categoryName = category.attrib["name"]
				traits = self.__readTraitData(category, species)
				for trait in traits:
					traitId = trait["id"]
					del trait["id"]
					self.__storage.addTrait( root.tag, categoryName, traitId, trait )


	def readSubPowers( self, root, species ):
		"""
		Lese die Unterkräfte aus den Template-Dateien.

		Diese werden zwar auch im trait-Dictionary gespeichert, haben aber andere Attribute als die normalen Eigenschaften.
		"""

		if root is not None:
			self.__storage.setSubPowerName(species, self.getElementAttribute(root, "name"))
			#Debug.debug(list(root))
			for categoryElement in list(root):
				if categoryElement.tag == "Category":
					categoryName = categoryElement.attrib["name"]
					## In diese Liste werden alle Unterkräfte geschrieben und erst wenn die gesamte Kategorie ausgelesen ist, werden selbige in den Speicher geschrieben.
					subPowerList = []
					cheap = []
					only = []
					for element in list(categoryElement):
						if element.tag == "trait":
							listOfPowers = {}
							listOfPrerequisites = []
							listOfOnlys = []
							for subelement in list(element):
								if subelement.tag == "power":
									listOfPowers.setdefault(subelement.text, int(subelement.attrib["value"]))
								elif subelement.tag == "prerequisites":
									listOfPrerequisites.append(u"({})".format(subelement.text))
								elif subelement.tag == "only":
									listOfOnlys.append(u"({})".format(subelement.text))
							powerPrerequisites = u" and ".join([u"Power.{} > {}".format(powerName, powerValue - 1) for powerName, powerValue in listOfPowers.items()])
							if powerPrerequisites:
								powerPrerequisites = u"({})".format(powerPrerequisites)
								listOfPrerequisites.append(powerPrerequisites)
							subPowerData = {
								"name": element.attrib["name"],
								"level": self.getElementAttribute(element, "level"),
								"species": species,
								"costFuel": self.getElementAttribute(element, "costFuel"),
								"costWill": self.getElementAttribute(element, "costWill"),
								"roll": self.getElementAttribute(element, "roll"),
								"powers": listOfPowers,
								"prerequisites": " and ".join(listOfPrerequisites),
								"cheap": [],
								"only": listOfOnlys,
							}
							#Debug.debug(subPowerData["name"], subPowerData["prerequisites"])
							identifier = self.getElementAttribute(element, "id")
							if not identifier:
								identifier = subPowerData["name"]
							subPowerList.append([
								categoryName,
								identifier,
								subPowerData,
							])
						elif element.tag == "cheap":
							cheap.append(element.text)
						elif element.tag == "only":
							only.append(element.text)
					#Debug.debug(subPowerList)
					for item in subPowerList:
						if cheap:
							item[2]["cheap"] = cheap
						if only:
							item[2]["only"] = only
						self.__storage.addTrait( root.tag, item[0], item[1], item[2] )


	def readCreationPoints( self, root, species ):
		"""
		Lese die Erschaffungspunkte aus, die den jeweiligen Spezies zur Verfügung stehen.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		if root is not None:
			for typElement in root.getiterator("Type"):
				typ = typElement.attrib["name"]
				resultList = []
				for pointsElement in typElement.getiterator("points"):
					points = int(pointsElement.attrib["value"])
					resultList.append(points)
				self.__storage.appendCreationPoints( species, typ, resultList )


	def readGroups( self, root, species ):
		"""
		Liest die verschiedenen Gruppierungsnamen der einzelnen Spezies ein.
		"""

		if root is not None:
			groupCategory = root.tag
			groupCategoryName = root.attrib["name"]
			self.__storage.appendTitle( species, groupCategory, groupCategoryName )
			for element in list(root):
				if element.tag == "item":
					#Debug.debug(element.tag, element.attrib["name"])
					groupName = element.attrib["name"]
					infos = {}
					for subElement in list(element):
						if subElement.tag == "kith":
							abilityList = []
							for subsubElement in list(subElement):
								if subsubElement.tag == "ability":
									abilityList.append(subsubElement.text)
							self.__storage.addKith(groupName, subElement.attrib["name"], " ".join(abilityList))
						elif subElement.tag == "weakness":
							infos["weakness"] = subElement.text
						elif subElement.tag == "blessing":
							infos["blessing"] = subElement.text
					self.__storage.appendTitle( species, groupCategory, groupCategoryName, element.attrib["name"], infos )


	def readPowerstat( self, root, species ):
		"""
		Lese die Informationen über die Auswirkungen der Supereigenschaft.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		if root is not None:
			#Debug.debug(root.tag)
			for element in root.getiterator("powerstat"):
				powerstatData = {
					"fuelMax": int(element.attrib["fuelMax"]),
					"fuelPerTurn": int(element.attrib["fuelPerTurn"]),
					"traitMax": int(element.attrib["traitMax"]),
				}
				powerstatValue = int(element.text)
				self.__storage.appendPowerstat( species, powerstatValue, powerstatData )


	def readDerangements( self, root, species ):
		"""
		Liest die Geistesstörungen aus den Template-Dateien.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		if root is not None:
			#Debug.debug(root.tag)
			for mildElement in root.getiterator("mild"):
				mild = mildElement.attrib["name"]
				descriptionMild = ""
				for descriptionElement in mildElement.getiterator("description"):
					descriptionMild = descriptionElement.text
				severeVersions = []
				for severeElement in mildElement.getiterator("severe"):
					severe = severeElement.attrib["name"]
					descriptionSevere = ""
					for descriptionElement in severeElement.getiterator("description"):
						descriptionSevere = descriptionElement.text
					self.__storage.appendDerangement(species=species, name=severe, dependancy=[], description=descriptionSevere, isSevere=True)
					severeVersions.append(severe)
				self.__storage.appendDerangement(species=species, name=mild, dependancy=severeVersions, description=descriptionMild, isSevere=False)


	def readWeapons(self, root):
		"""
		Einlesen der Waffen.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		for Weapons in root:
			if GlobalState.isFallback or not self.getElementAttribute(Weapons, "fallback") == "True":
				for typElement in Weapons.getiterator("Type"):
					typeName = self.getElementAttribute(typElement, "name")
					for categoryElement in typElement.getiterator("Category"):
						for weaponElement in typElement.getiterator("weapon"):
							#Debug.debug(weaponElement.attrib["name"])
							weaponName = weaponElement.attrib["name"]
							weaponData = {
								"damage": self.getElementAttribute(weaponElement, "damage"),
								"ranges": self.getElementAttribute(weaponElement, "ranges"),
								"capacity": self.getElementAttribute(weaponElement, "capacity"),
								"strength": self.getElementAttribute(weaponElement, "strength"),
								"size": self.getElementAttribute(weaponElement, "size"),
								"durability": self.getElementAttribute(weaponElement, "durability"),
							}
							self.__storage.addWeapon( typeName, weaponName, weaponData )


	def readArmor(self, root):
		"""
		Einlesen der Rüstungen.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		for Armor in root:
			if GlobalState.isFallback or not self.getElementAttribute(Armor, "fallback") == "True":
				for armorElement in Armor.getiterator("armor"):
					armorName = armorElement.attrib["name"]
					armorData = {
						"general": int(self.getElementAttribute(armorElement, "general")),
						"firearms": int(self.getElementAttribute(armorElement, "firearms")),
						"defense": int(self.getElementAttribute(armorElement, "defense")),
						"speed": int(self.getElementAttribute(armorElement, "speed")),
					}
					self.__storage.addArmor( armorName, armorData )


	def readEquipment(self, root):
		"""
		Einlesen der Ausrüstung.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()
		"""

		for Equipment in root:
			if GlobalState.isFallback or not self.getElementAttribute(Equipment, "fallback") == "True":
				for equipmentElement in Equipment.getiterator("equipment"):
					equipmentName = equipmentElement.attrib["name"]
					equipmentData = {
						"durability": int(self.getElementAttribute(equipmentElement, "durability")),
						"size": int(self.getElementAttribute(equipmentElement, "size")),
						"cost": int(self.getElementAttribute(equipmentElement, "cost")),
					}
					self.__storage.addEquipment( equipmentName, equipmentData )


	def __readTraitData(self, root, species=None, typ=None, category=None):
		"""
		Einlesen aller Eigenschaftswerte.

		Gibt ein Dictionary folgender Form zurück:

		{
			"typ": <Typ der ausgelsenen Eigenschaften>,
			"traits" [<Liste der Eigenschaftsdaten der gefundenen Eigenschaften>]
		}

		\todo Eine Eigenschaft kann mehrfach vorkommen, da andere Spezies andere Spezialisierungen mitbringen mögen.

		\todo Ersetze getiterator durch list(elem) oder Element.iter()

		\todo Dictionary-keys "cheap" und "only" werden nicht ausgelesen sondern nur als [] gesetzt.
		"""

		listOfTraits = []
		if root is not None:
			for traitElement in root.getiterator("trait"):
				listOfSpecialties = []
				for traitSubElement in traitElement.getiterator("specialty"):
					listOfSpecialties.append(traitSubElement.text)
				listOfSpecialties.sort()
				listOfPrerequisites = []
				for traitSubElement in traitElement.getiterator("prerequisites"):
					listOfPrerequisites.append(traitSubElement.text)
				listOfValues = []
				for traitSubElement in traitElement.getiterator("value"):
					listOfValues.append(int(traitSubElement.text))
				traitData = {
					"id": self.getElementAttribute(traitElement, "id"),			# Einzigartiger Identifier der Eigenschaft. Ist meist identisch mit dem Namen.
					"name": traitElement.attrib["name"],							# Name der Eigenschaft (alle)
					"level": self.getElementAttribute(traitElement, "level"),		# Stufe der Eigenschaft (Subpowers)
					"values": [0],													# Erlaubte Werte, welche diese Eigenschaft annehmen kann. (Merits)
					"species": species,												# Die Spezies, für welche diese Eigenschaft zur Verfügung steht.
					"age": self.getElementAttribute(traitElement, "age"),			# Die Alterskategorie, für welche diese Eigenschaft zur Verfügung steht.
					"era": self.getElementAttribute(traitElement, "era"),			# Die Zeitalterkategorie, für welche diese Eigenschaft zur Verfügung steht.
					"custom": self.getElementAttribute(traitElement, "custom"),	# Handelt es sich um eine Kraft mit Zusatztext?
					"specialties": listOfSpecialties,									# Dieser Eigenschaft zugeteilten Spezialisierungen (Skills)
					"prerequisites": " and ".join(listOfPrerequisites),				# Voraussetzungen für diese Eigenschaft (Merits, Subpowers)
					"cheap": [],
					"only": [],
				}
				if not traitData["id"]:
					traitData["id"] = traitData["name"]
				traitData["values"].extend(listOfValues)
				listOfTraits.append(traitData)

		return listOfTraits


