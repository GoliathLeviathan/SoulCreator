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

from PySide.QtCore import Qt, QDate, Signal
from PySide.QtGui import QWidget, QIcon, QLabel

from src.Config import Config
from src.Datatypes.Identity import Identity
#from src.Widgets.Components.CharaSpecies import CharaSpecies
from src.Widgets.Dialogs.NameDialog import NameDialog
from src.Debug import Debug

from ui.ui_InfoWidget import Ui_InfoWidget




class InfoWidget(QWidget):
	"""
	@brief Das Widget, in welchem wichtige Informationen dargestellt werden.

	Spezies, Namen etc. des Charakters werden hier dargestellt.

	\note Der Beschreibungstext wird nur gespeichert, wenn das Textfeld, indem er eingetragen wird, den Fokus verliert. Müßte aber ausreichen, da ihm bspw. schon das Speichern den Fokus raubt.
	"""


	nameChanged = Signal(str)


	def __init__(self, template, character, parent=None):
		QWidget.__init__(self, parent)

		self.ui = Ui_InfoWidget()
		self.ui.setupUi(self)
		
		self.__storage = template
		self.__character = character

		# Die zweite Spalte darf sich strecken.
		self.ui.layout_main.setColumnStretch(1, 1)
		# Labels werden rechtsbündig gesetzt.
		for i in range(self.ui.layout_main.columnCount())[::3]:
			for j in xrange(self.ui.layout_main.rowCount()):
				item = self.ui.layout_main.itemAtPosition(j, i)
				if item != None and type(item.widget()) == QLabel:
					item.widget().setAlignment(Qt.AlignRight)

		for item in Config.genders:
			self.ui.comboBox_gender.addItem( QIcon(item[1]), item[0] )

		speciesList = self.__storage.species.keys()
		speciesList.sort()
		self.ui.comboBox_species.addItems(speciesList)

		self.ui.comboBox_era.addItems( Config.eras )

		## Speichern der vom Benutzer veränderten Werte
		self.ui.pushButton_name.clicked.connect(self.openNameDialog)
		self.ui.comboBox_era.currentIndexChanged[str].connect(self.changeEra)
		self.ui.comboBox_gender.currentIndexChanged[str].connect(self.changeGender)
		self.ui.dateEdit_dateBirth.dateChanged.connect(self.changeDateBirth)
		self.ui.dateEdit_dateBecoming.dateChanged.connect(self.changeDateBecoming)
		self.ui.dateEdit_dateGame.dateChanged.connect(self.changeDateGame)
		self.ui.comboBox_species.currentIndexChanged[str].connect(self.changeSpecies)
		self.ui.comboBox_virtue.currentIndexChanged[str].connect(self.changeVirtue)
		self.ui.comboBox_vice.currentIndexChanged[str].connect(self.changeVice)
		self.ui.comboBox_breed.currentIndexChanged[str].connect(self.changeBreed)
		self.ui.comboBox_faction.currentIndexChanged[str].connect(self.changeFaction)
		self.ui.lineEdit_faction.textEdited.connect(self.changeFaction)
		self.ui.comboBox_organisation.currentIndexChanged[str].connect(self.changeOrganisation)
		self.ui.lineEdit_party.textEdited.connect(self.changeParty)
		#self.ui.textEdit_description.textChanged.connect(self.saveDescription)	## Kann ich nicht nutzen, da sonst der Curser bei jeder änderung an den Angang springt.
		self.ui.textEdit_description.focusLost.connect(self.changeDescription)

		## Aktualisieren der Darstellung der im Charakter veränderten Werte.
		self.__character.identities[0].nameChanged.connect(self.updateName)
		self.__character.identities[0].genderChanged[str].connect(self.updateGender)
		self.__character.eraChanged.connect(self.updateEra)
		self.__character.dateBirthChanged.connect(self.updateDateBirth)
		self.__character.dateBecomingChanged.connect(self.updateDateBecoming)
		self.__character.dateGameChanged.connect(self.updateDateGame)
		self.__character.ageChanged.connect(self.updateAge)
		self.__character.ageBecomingChanged.connect(self.updateAgeBecoming)
		self.__character.speciesChanged.connect(self.updateSpecies)
		self.__character.virtueChanged.connect(self.updateVirtue)
		self.__character.viceChanged.connect(self.updateVice)
		self.__character.breedChanged.connect(self.updateBreed)
		self.__character.speciesChanged.connect(self.updateBreedTitle)
		self.__character.speciesChanged.connect(self.repopulateBreeds)
		self.__character.factionChanged.connect(self.updateFaction)
		self.__character.speciesChanged.connect(self.updateFactionTitle)
		self.__character.speciesChanged.connect(self.repopulateFactions)
		self.__character.organisationChanged.connect(self.updateOrganisation)
		self.__character.speciesChanged.connect(self.updateOrganisationTitle)
		self.__character.speciesChanged.connect(self.repopulateOrganisations)
		self.__character.partyChanged.connect(self.updateParty)
		self.__character.speciesChanged.connect(self.updatePartyTitle)
		self.__character.descriptionChanged.connect(self.updateDescription)
		# Menschen können ihre Fraktion selbst eintragen und haben einige Angaben einfach nicht nötig.
		self.__character.speciesChanged.connect(self.hideShowWidgets_species)

		## Ändert sich das Alter, gibt es andere Virtues und Vices.
		self.__character.ageChanged.connect(self.repopulateVirtues)
		self.__character.ageChanged.connect(self.repopulateVices)


	def openNameDialog(self):
		"""
		Ruft einen Dialog auf, in welchem die zahlreichen Namen des Charakters eingetragen werden können.
		"""
		
		dialog = NameDialog( self.__character, self )
		dialog.exec_()


	def changeEra( self, era ):
		"""
		Legt die zeitliche Ära fest, in welcher der Charakter zuhause ist.
		"""

		self.__character.era = era


	def changeGender( self, gender ):
		"""
		Legt das Geschlecht des Charakters fest.
		"""

		self.__character.identities[0].gender = gender


	def changeDateBirth( self, date ):
		"""
		Legt den Geburtstag des Charakters fest.
		"""

		self.__character.dateBirth = date


	def changeDateBecoming( self, date ):
		"""
		Legt den Tag fest, an welchem der Charakters zu etwas Übernatürlichem verändert wurde.
		"""

		self.__character.dateBecoming = date


	def changeDateGame( self, date ):
		"""
		Legt das Datum des Spiels fest.
		"""

		self.__character.dateGame = date


	def changeSpecies( self, species ):
		"""
		Verändert die Spezies des Charakters.
		"""

		self.__character.species = species


	def changeVirtue( self, virtue ):
		"""
		Verändert die Tugend des Charakters.
		"""

		self.__character.virtue = virtue


	def changeVice( self, vice ):
		"""
		Verändert das Laster des Charakters.
		"""

		self.__character.vice = vice


	def changeBreed( self, breed ):
		"""
		Verändert die Brut des Charakters.
		"""

		self.__character.breed = breed


	def changeFaction( self, faction ):
		"""
		Verändert die Fraktion des Charakters.
		"""

		self.__character.faction = faction


	def changeOrganisation( self, organisation ):
		"""
		Verändert die Organisation (Blutlinie etc.) des Charakters.
		"""

		self.__character.organisation = organisation


	def changeParty( self, name ):
		"""
		Verändert den Namen der Freundesgruppe.
		"""

		self.__character.party = name


	def changeDescription( self ):
		"""
		Verändert den Beschreibungstext im Speicher.
		"""

		self.__character.description = self.ui.textEdit_description.toPlainText()


	def updateName( self ):
		"""
		Aktualisiert die Anzeige des Namens.
		"""

		nameStr = Identity.displayNameDisplay(self.__character.identities[0].surename, self.__character.identities[0].firstname, self.__character.identities[0].nickname)
		nameDisplay = nameStr
		if not nameStr:
			nameStr = self.tr("Name")
		self.ui.pushButton_name.setText( nameStr )
		self.nameChanged.emit(nameDisplay)


	def updateEra(self, era):
		"""
		Aktualisiert die Anzeige der Ära
		"""

		#Debug.debug("Verändere Anzeige der Ära auf {}".format(era))
		self.ui.comboBox_era.setCurrentIndex(self.ui.comboBox_era.findText(era))


	def updateGender( self, gender ):
		"""
		Aktualisiert die Anzeige des Geschlechts.
		"""

		self.ui.comboBox_gender.setCurrentIndex( self.ui.comboBox_gender.findText(gender))


	def updateDateBirth(self, date):
		"""
		Aktualisiert die Anzeige des Geburtstages.
		"""

		self.ui.dateEdit_dateBirth.setDate(date)


	def updateDateBecoming(self, date):
		"""
		Aktualisiert die Anzeige des Datums der Verwandlung zu etwas Übernatürlichem.
		"""

		self.ui.dateEdit_dateBecoming.setDate(date)


	def updateDateGame(self, date):
		"""
		Aktualisiert die Anzeige des Datums im Spiel.
		"""

		self.ui.dateEdit_dateGame.setDate(date)


	def updateAge(self, age):
		"""
		Aktualisiert die Anzeige des Alters.
		"""

		self.ui.label_age.setNum(age)


	def updateAgeBecoming(self, age):
		"""
		Aktualisiert die Anzeige des Alters bei der Veränderung.
		"""

		self.ui.label_ageBecoming.setNum(age)


	def updateSpecies( self, species ):
		"""
		Aktualisiert die Anzeige der Spezies.
		"""

		self.ui.comboBox_species.setCurrentIndex( self.ui.comboBox_species.findText( species ) )


	def updateVirtue( self, virtue ):
		"""
		Aktualisiert die Anzeige der Tugend.
		"""

		self.ui.comboBox_virtue.setCurrentIndex( self.ui.comboBox_virtue.findText( virtue ) )


	def updateVice( self, vice ):
		"""
		Aktualisiert die Anzeige des Lasters.
		"""

		self.ui.comboBox_vice.setCurrentIndex( self.ui.comboBox_vice.findText( vice ) )


	def updateBreed( self, breed ):
		"""
		Aktualisiert die Anzeige der Brut.
		"""

		self.ui.comboBox_breed.setCurrentIndex( self.ui.comboBox_breed.findText( breed ) )


	def updateBreedTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Bruten.
		"""

		self.ui.label_breed.setText( "{}:".format(self.__storage.breedTitle(species)) )


	def updateFaction( self, faction ):
		"""
		Aktualisiert die Anzeige der Fraktion.
		"""

		self.ui.comboBox_faction.setCurrentIndex( self.ui.comboBox_faction.findText( faction ) )


	def updateFactionTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Fraktionen
		"""

		self.ui.label_faction.setText( "{}:".format(self.__storage.factionTitle(species)) )


	def updateOrganisation( self, organisation ):
		"""
		Aktualisiert die Anzeige der Organisation (Ritterorden, Legate, Blutlinien, etc.).

		\todo Um einer Organisation beizutreten sind gewisse Anforderungen zu erfüllen. Diese sollten in das programm irgendwie eingebaut werden.
		"""

		self.ui.comboBox_organisation.setCurrentIndex( self.ui.comboBox_organisation.findText( organisation ) )


	def updateOrganisationTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Fraktionen
		"""

		self.ui.label_organisation.setText( "{}:".format(self.__storage.organisationTitle(species)) )


	def updateParty( self, name ):
		"""
		Aktualisiert die Anzeige der Freundesgruppe.
		"""

		self.ui.lineEdit_party.setText( self.__character.party )


	def updatePartyTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Freundesgruppe.
		"""

		self.ui.label_party.setText( "{}:".format(self.__storage.partyTitle(species)) )


	def updateDescription( self, text ):
		"""
		Aktualisiert die Anzeige des Beschreibungstextes.
		"""

		self.ui.textEdit_description.setPlainText( self.__character.description )


	def repopulateVirtues(self, age):
		ageStr = Config.ages[0]
		if age < Config.adultAge:
			ageStr = Config.ages[1]

		virtueList = []
		for item in self.__storage.virtues:
			if item["age"] == ageStr:
				virtueList.append(item["name"])

		self.ui.comboBox_virtue.clear()
		self.ui.comboBox_virtue.addItems(virtueList)


	def repopulateVices(self, age):
		ageStr = Config.ages[0]
		if age < Config.adultAge:
			ageStr = Config.ages[1]

		viceList = []
		for item in self.__storage.vices:
			if item["age"] == ageStr:
				viceList.append(item["name"])

		self.ui.comboBox_vice.clear()
		self.ui.comboBox_vice.addItems(viceList)


	def repopulateBreeds(self, species):

		self.ui.comboBox_breed.clear()
		self.ui.comboBox_breed.addItems(self.__storage.breeds(species))


	def repopulateFactions(self, species):

		self.ui.comboBox_faction.clear()
		self.ui.comboBox_faction.addItems(self.__storage.factions(species))


	def repopulateOrganisations(self, species):

		self.ui.comboBox_organisation.clear()
		self.ui.comboBox_organisation.addItems(self.__storage.organisations(species))


	def hideShowWidgets_species(self, species):

		visible = True
		if species == "Human":
			visible = False

		## Menschen haben keinen Tag der Verwandlung.
		self.ui.label_dateBecoming.setVisible(visible)
		self.ui.dateEdit_dateBecoming.setVisible(visible)
		self.ui.label_ageBecoming_label.setVisible(visible)
		self.ui.label_ageBecoming.setVisible(visible)

		self.ui.label_breed.setVisible(visible)
		self.ui.comboBox_breed.setVisible(visible)
		self.ui.label_organisation.setVisible(visible)
		self.ui.comboBox_organisation.setVisible(visible)

		self.ui.comboBox_faction.setVisible( visible )
		self.ui.lineEdit_faction.setVisible( not visible )
		self.ui.lineEdit_faction.clear()



