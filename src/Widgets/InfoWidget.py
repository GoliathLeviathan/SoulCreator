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

from PySide.QtCore import Qt, QSize, QFile, QDate, Signal
from PySide.QtGui import QWidget, QIcon, QLabel, QPixmap, QFileDialog, QMessageBox

from src.Config import Config
from src.Tools import PathTools
from src.Calc.Calc import Calc
from src.Datatypes.Identity import Identity
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

		self.__age = 0

		speciesList = self.__storage.species.keys()
		speciesList.sort()
		#self.ui.comboBox_species.addItems(speciesList)
		for species in speciesList:
			self.ui.comboBox_species.addItem(QIcon(":/icons/images/Skull-{}.png".format(species)), species)

		self.ui.comboBox_era.addItems( Config.eras )

		self.ui.dateEdit_dateBirth.setMinimumDate(QDate(100, 1, 1))
		self.ui.dateEdit_dateBecoming.setMinimumDate(QDate(100, 1, 1))
		self.ui.dateEdit_dateGame.setMinimumDate(QDate(100, 1, 1))

		self.ui.pushButton_pictureClear.setIcon(QIcon(":/icons/images/actions/cancel.png"))
		self.ui.pushButton_pictureClear.setText("")
		self.ui.pushButton_pictureClear.setEnabled(False)

		## Speichern der vom Benutzer veränderten Werte
		self.ui.pushButton_name.clicked.connect(self.openNameDialog)
		self.ui.comboBox_era.currentIndexChanged[str].connect(self.__character.setEra)
		#self.ui.dateEdit_dateBirth.dateChanged.connect(self.setCharacterDateBirth)
		self.ui.dateEdit_dateBirth.dateEdited.connect(self.setCharacterDateBirth)
		self.ui.dateEdit_dateBecoming.dateChanged.connect(self.__character.setDateBecoming)
		#self.ui.dateEdit_dateGame.dateChanged.connect(self.setCharacterDateGame)
		self.ui.dateEdit_dateGame.dateEdited.connect(self.setCharacterDateGame)
		self.ui.comboBox_species.currentIndexChanged[str].connect(self.__character.setSpecies)
		self.ui.comboBox_virtue.currentIndexChanged[str].connect(self.__character.setVirtue)
		self.ui.comboBox_vice.currentIndexChanged[str].connect(self.__character.setVice)
		self.ui.comboBox_breed.currentIndexChanged[str].connect(self.__character.setBreed)
		self.ui.comboBox_kith.currentIndexChanged[str].connect(self.__character.setKith)
		self.ui.comboBox_faction.currentIndexChanged[str].connect(self.__character.setFaction)
		self.ui.lineEdit_faction.textEdited.connect(self.__character.setFaction)
		self.ui.comboBox_organisation.currentIndexChanged[str].connect(self.__character.setOrganisation)
		self.ui.lineEdit_party.textEdited.connect(self.__character.setParty)
		self.ui.doubleSpinBox_height.valueChanged[float].connect(self.__character.setHeight)
		self.ui.spinBox_weight.valueChanged[int].connect(self.__character.setWeight)
		self.ui.lineEdit_eyes.textEdited.connect(self.__character.setEyes)
		self.ui.lineEdit_hair.textEdited.connect(self.__character.setHair)
		self.ui.lineEdit_nationality.textEdited.connect(self.__character.setNationality)
		self.ui.pushButton_picture.clicked.connect(self.openImage)
		self.ui.pushButton_pictureClear.clicked.connect(self.clearImage)
		#self.ui.textEdit_description.textChanged.connect(self.saveDescription)	## Kann ich nicht nutzen, da sonst der Curser bei jeder änderung an den Angang springt.
		self.ui.textEdit_description.focusLost.connect(self.changeDescription)

		## Aktualisieren der Darstellung der im Charakter veränderten Werte.
		self.__character.identity.identityChanged.connect(self.updateButtonText)
		self.__character.eraChanged.connect(self.updateEra)
		self.__character.dateBirthChanged.connect(self.ui.dateEdit_dateBirth.setDate)
		self.__character.dateBecomingChanged.connect(self.ui.dateEdit_dateBecoming.setDate)
		self.__character.dateGameChanged.connect(self.ui.dateEdit_dateGame.setDate)
		self.__character.ageChanged.connect(self.ui.label_age.setNum)
		self.__character.ageBecomingChanged.connect(self.ui.label_ageBecoming.setNum)
		self.__character.speciesChanged.connect(self.updateSpecies)
		self.__character.virtueChanged.connect(self.updateVirtue)
		self.__character.viceChanged.connect(self.updateVice)
		self.__character.breedChanged.connect(self.updateBreed)
		self.__character.breedChanged.connect(self.repopulateKiths)
		#self.__character.speciesChanged.connect(self.repopulateKiths)
		self.__character.kithChanged.connect(self.updateKith)
		self.__character.speciesChanged.connect(self.updateBreedTitle)
		self.__character.speciesChanged.connect(self.repopulateBreeds)
		self.__character.factionChanged.connect(self.updateFaction)
		self.__character.speciesChanged.connect(self.updateFactionTitle)
		self.__character.speciesChanged.connect(self.repopulateFactions)
		self.__character.organisationChanged.connect(self.updateOrganisation)
		self.__character.speciesChanged.connect(self.updateOrganisationTitle)
		self.__character.speciesChanged.connect(self.repopulateOrganisations)
		self.__character.partyChanged.connect(self.ui.lineEdit_party.setText)
		self.__character.speciesChanged.connect(self.updatePartyTitle)
		self.__character.heightChanged.connect(self.ui.doubleSpinBox_height.setValue)
		self.__character.weightChanged.connect(self.ui.spinBox_weight.setValue)
		self.__character.eyesChanged.connect(self.ui.lineEdit_eyes.setText)
		self.__character.hairChanged.connect(self.ui.lineEdit_hair.setText)
		self.__character.nationalityChanged.connect(self.ui.lineEdit_nationality.setText)
		self.__character.pictureChanged.connect(self.updatePicture)
		self.__character.descriptionChanged.connect(self.ui.textEdit_description.setPlainText)
		# Menschen können ihre Fraktion selbst eintragen und haben einige Angaben einfach nicht nötig.
		self.__character.speciesChanged.connect(self.hideShowWidgets_species)

		## Das Alter darf nie negativ werden können
		self.ui.dateEdit_dateBirth.dateChanged.connect(self.ui.dateEdit_dateBecoming.setMinimumDate)
		self.ui.dateEdit_dateGame.dateChanged.connect(self.setMaxBirthday)

		## Ändert sich das Alter, gibt es andere Virtues und Vices.
		self.__character.ageChanged.connect(self.updateVirtueTitle)
		self.__character.ageChanged.connect(self.repopulateVirtues)
		self.__character.ageChanged.connect(self.updateViceTitle)
		self.__character.ageChanged.connect(self.repopulateVices)

		self.__character.ageChanged.connect(self.setAge)



	def openNameDialog(self):
		"""
		Ruft einen Dialog auf, in welchem die zahlreichen Namen des Charakters eingetragen werden können.
		"""

		dialog = NameDialog( self.__character, self )
		dialog.exec_()


	def changeDescription( self ):
		"""
		Verändert den Beschreibungstext im Speicher.
		"""

		self.__character.description = self.ui.textEdit_description.toPlainText()


	def updateButtonText( self ):
		"""
		Aktualisiert die Anzeige des Namens.
		"""

		nameStr = Identity.displayNameDisplay(self.__character.identity.surname, self.__character.identity.firstname, self.__character.identity.nickname)
		nameDisplay = nameStr
		if not nameStr:
			nameStr = self.tr("Name")
		self.ui.pushButton_name.setText( nameStr )
		genderIcon = QIcon()
		for item in Config.genders:
			if self.__character.identity.gender == item[0]:
				self.ui.pushButton_name.setIcon(QIcon(item[1]))
				break
		self.nameChanged.emit(nameDisplay)


	def updateEra(self, era):
		"""
		Aktualisiert die Anzeige der Ära
		"""

		#Debug.debug("Verändere Anzeige der Ära auf {}".format(era))
		self.ui.comboBox_era.setCurrentIndex(self.ui.comboBox_era.findText(era))


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


	def updateKith( self, kith ):
		"""
		Aktualisiert die Anzeige des Kith.
		"""

		self.ui.comboBox_kith.setCurrentIndex( self.ui.comboBox_kith.findText( kith ) )


	def updateFaction( self, faction ):
		"""
		Aktualisiert die Anzeige der Fraktion.
		"""

		self.ui.lineEdit_faction.setText(faction)
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


	def updatePartyTitle( self, species ):
		"""
		Wenn die Spezies sich ändert, ändert sich auch der Bezeichner für die Freundesgruppe.
		"""

		self.ui.label_party.setText( "{}:".format(self.__storage.partyTitle(species)) )


	def updateVirtueTitle( self, age ):
		"""
		Wenn die Alterskategorie sich ändert, ändert sich auch der Bezeichner für die Tugenden.
		"""

		label = self.tr("Virtue")
		if age < Config.ageAdult:
			label = self.tr("Asset")
		if self.ui.label_virtue.text() != label:
			self.ui.label_virtue.setText( "{}:".format(label) )


	def updateViceTitle( self, age ):
		"""
		Wenn die Alterskategorie sich ändert, ändert sich auch der Bezeichner für die Laster.
		"""

		label = self.tr("Vice")
		if age < Config.ageAdult:
			label = self.tr("Fault")
		if self.ui.label_vice.text() != label:
			self.ui.label_vice.setText( "{}:".format(label) )


	def repopulateVirtues(self, age):
		ageStr = Config.ages[0]
		if age < Config.ageAdult:
			ageStr = Config.ages[1]

		virtueList = []
		for item in self.__storage.virtues:
			if item["age"] == ageStr:
				virtueList.append(item["name"])

		## Die Liste soll nur aktualisiert werden, wenn eine neue Alterskategorie erreicht wird.
		if self.ui.comboBox_virtue.itemText(0) not in virtueList:
			self.ui.comboBox_virtue.clear()
			self.ui.comboBox_virtue.addItems(virtueList)


	def repopulateVices(self, age):
		ageStr = Config.ages[0]
		if age < Config.ageAdult:
			ageStr = Config.ages[1]

		viceList = []
		for item in self.__storage.vices:
			if item["age"] == ageStr:
				viceList.append(item["name"])

		## Die Liste soll nur aktualisiert werden, wenn eine neue Alterskategorie erreicht wird.
		if self.ui.comboBox_vice.itemText(0) not in viceList:
			self.ui.comboBox_vice.clear()
			self.ui.comboBox_vice.addItems(viceList)


	def repopulateBreeds(self, species):

		self.ui.comboBox_breed.clear()
		self.ui.comboBox_breed.addItems(self.__storage.breeds(species))


	def repopulateKiths(self, breed):
		"""
		Jedes Seeming hat eine Reihe möglicher Kiths. Kiths stehen nur Changelings offen.
		"""

		self.ui.comboBox_kith.clear()
		if breed and self.__character.species == "Changeling":
			#Debug.debug(breed)
			self.ui.comboBox_kith.addItems(self.__storage.kiths(breed))


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

		## Das Kith ist nur für Changelings interessant
		if species == "Changeling":
			self.ui.label_kith.setVisible(True)
			self.ui.comboBox_kith.setVisible(True)
		else:
			self.ui.label_kith.setVisible(False)
			self.ui.comboBox_kith.setVisible(False)


	def openImage(self ):
		"""
		Öffnet einen Dialog zum Laden eines Charakterbildes und speichert selbiges im Charakter-Speicher.

		\note Das Bild wird auf eine in der Configurationsdatei festgelegte Maximalgröße skaliert, um die Größe überschaubar zu halten.
		"""

		appPath = PathTools.getPath()

		# Pfad zum Speicherverzeichnis
		savePath = ""
		if os.name == "nt":
			savePath = os.environ['HOMEPATH']
		else:
			savePath = os.environ['HOME']

		# Wenn Unterverzeichnis nicht existiert, suche im Programmverzeichnis.
		if ( not os.path.exists( savePath ) ):
			savePath = appPath

		filePath = QFileDialog.getOpenFileName(
			self,
			self.tr( "Select Image File" ),
			savePath,
			self.tr( "Images (*.jpg *.jpeg *.png *.bmp *.gif *.pgm *.pbm *.ppm *.svg )" )
		)

		if ( filePath[0] ):
			image = QPixmap(filePath[0])
			if image.width() > Config.pictureWidthMax or image.height() > Config.pictureHeightMax:
				image = image.scaled(800, 800, Qt.KeepAspectRatio)

			self.updatePicture(image)

			self.__character.picture = image


	def clearImage(self):
		"""
		Löscht das Charakterbild.
		"""

		self.__character.picture = QPixmap()


	def updatePicture(self, image):
		"""
		Stellt das Charakterbild dar.
		"""

		if image.isNull():
			self.ui.pushButton_picture.setIcon(QIcon())
			self.ui.pushButton_picture.setText("Open Picture")
			self.ui.pushButton_pictureClear.setEnabled(False)
		else:
			self.ui.pushButton_picture.setText("")
			self.ui.pushButton_picture.setIcon(image)
			self.ui.pushButton_pictureClear.setEnabled(True)


	def setAge(self, age):
		if self.__age != age:
			self.__age = age


	def setCharacterDateBirth(self, date):
		"""
		Speichert das Geburtsdatum des Charakters im Speicher.

		Allerdings muß zuvor möglicherweise um Erlaubnis gefragt werden.
		"""

		years = Calc.years(self.ui.dateEdit_dateGame.date(), self.ui.dateEdit_dateBirth.date())
		if self.__age != years:
			if (self.__age < Config.ageAdult <= years or years < Config.ageAdult <= self.__age) and not self.warnAgeChange(years, self.__age):
				self.ui.dateEdit_dateBirth.setDate(self.ui.dateEdit_dateGame.date().addYears(-1 * self.__age))
			else:
				self.__character.setDateBirth(date)


	def setCharacterDateGame(self, date):
		"""
		Speichert das Geburtsdatum des Charakters im Speicher.

		Allerdings muß zuvor möglicherweise um Erlaubnis gefragt werden.
		"""

		years = Calc.years(self.ui.dateEdit_dateGame.date(), self.ui.dateEdit_dateBirth.date())
		if self.__age != years:
			if (self.__age < Config.ageAdult <= years or years < Config.ageAdult <= self.__age) and not self.warnAgeChange(years, self.__age):
				self.ui.dateEdit_dateGame.setDate(self.ui.dateEdit_dateBirth.date().addYears(self.__age))
			else:
				self.__character.setDateGame(date)


	def warnAgeChange(self, newAge, oldAge):
		"""
		Wird der Charakter vom Erwachsenen zum Kind (oder umgekehrt), sollte eine Bestätigung eingefordert werden.

		Wird auf "No" geklickt, wird das Geburtsdatum wieder so verändert, daß das alte Alter beibehalten bleibt.

		\bug Aber dadurch wird automatisch die Frage erneut gestellt, nur diesmal andersherum. Wie ändere ich das.
		"""

		text = self.tr("Your character is going to be an adult.")
		if newAge < Config.ageAdult:
			text = self.tr("Your character is going to be a child.")
		ret = QMessageBox.warning(
			self,
			self.tr( "Age category changed" ),
			self.tr( "{} Do you want that to happen?".format(text) ),
			QMessageBox.Yes | QMessageBox.No
		)
		if ret == QMessageBox.StandardButton.No:
			return False
		else:
			return True


	def setMaxBirthday(self):
		"""
		Ändert sich die Zeit im Spiel, ändert sich das maximal einzustellende Geburtsdatum, so daß der Charakter nicht jünger sein kann als der vorgegebene Minimalwert.
		"""

		maxDateBirth = self.ui.dateEdit_dateGame.date().addYears(-1 * Config.ageMin)
		self.ui.dateEdit_dateBirth.setMaximumDate(maxDateBirth)
		self.ui.dateEdit_dateBecoming.setMaximumDate(self.ui.dateEdit_dateGame.date())
