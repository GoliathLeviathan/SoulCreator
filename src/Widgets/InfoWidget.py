# -*- coding: utf-8 -*-

"""
# Copyright

Copyright (C) 2012 by Victor
victor@caern.de

# License

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




import os

from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import Qt, QDate
from PyQt4.QtGui import QWidget, QIcon, QPixmap, QFileDialog, QMessageBox

import src.Config as Config
import src.Tools.PathTools as PathTools
#from src.Calc.Calc import Calc
from src.Datatypes.Identity import Identity
from src.Widgets.Dialogs.NameDialog import NameDialog
#import src.Debug as Debug

from ui.ui_InfoWidget import Ui_InfoWidget




class InfoWidget(QWidget):
	"""
	@brief Das Widget, in welchem wichtige Informationen dargestellt werden.

	Namen, Alter, Nationalität etc. des Charakters werden hier dargestellt.

	\note Der Beschreibungstext wird nur gespeichert, wenn das Textfeld, indem er eingetragen wird, den Fokus verliert. Müßte aber ausreichen, da ihm bspw. schon das Speichern den Fokus raubt.
	"""


	nameChanged = Signal(str)
	notificationSent = Signal(str)


	def __init__(self, template, character, parent=None):
		super(InfoWidget, self).__init__(parent)

		self.ui = Ui_InfoWidget()
		self.ui.setupUi(self)

		self.__storage = template
		self.__character = character

		self.ui.comboBox_era.addItems( list(Config.ERAS.keys()) )

		self.ui.dateEdit_dateBirth.setMinimumDate(QDate(100, 1, 1))
		self.ui.dateEdit_dateGame.setMinimumDate(QDate(100, 1, 1))

		self.ui.pushButton_pictureClear.setIcon(QIcon(":/icons/images/actions/cancel.png"))
		self.ui.pushButton_pictureClear.setText("")
		self.ui.pushButton_pictureClear.setEnabled(False)

		## Speichern der vom Benutzer veränderten Werte
		self.ui.pushButton_name.clicked.connect(self.openNameDialog)
		self.ui.comboBox_era.currentIndexChanged[str].connect(self.updateDateGame_era)
		#self.ui.dateEdit_dateBirth.dateEdited.connect(self.setCharacterDateBirth)
		#self.ui.dateEdit_dateGame.dateEdited.connect(self.setCharacterDateGame)
		#self.ui.dateEdit_dateGame.dateEdited.connect(self.setCharacterEra)
		self.ui.dateEdit_dateBirth.dateChanged.connect(self.setCharacterDateBirth)
		self.ui.dateEdit_dateGame.dateChanged.connect(self.setCharacterDateGame)
		self.ui.dateEdit_dateGame.dateChanged.connect(self.setCharacterEra)
		self.ui.comboBox_virtue.currentIndexChanged[str].connect(self.__character.setVirtue)
		self.ui.comboBox_vice.currentIndexChanged[str].connect(self.__character.setVice)
		self.ui.doubleSpinBox_height.valueChanged[float].connect(self.setCharacterHeight)
		self.ui.spinBox_weight.valueChanged[int].connect(self.__character.setWeight)
		self.ui.lineEdit_eyes.textEdited.connect(self.__character.setEyes)
		self.ui.lineEdit_hair.textEdited.connect(self.__character.setHair)
		self.ui.lineEdit_nationality.textEdited.connect(self.__character.setNationality)
		self.ui.pushButton_picture.clicked.connect(self.openImage)
		self.ui.pushButton_pictureClear.clicked.connect(self.clearImage)
		#self.ui.textEdit_description.textChanged.connect(self.saveDescription)	## Kann ich nicht nutzen, da sonst der Curser bei jeder änderung an den Angang springt.
		self.ui.textEdit_description.textChanged.connect(self.changeDescription)

		## Aktualisieren der Darstellung der im Charakter veränderten Werte.
		self.__character.identity.identityChanged.connect(self.updateButtonText)
		self.__character.eraChanged.connect(self.updateEra)
		self.__character.dateBirthChanged.connect(self.ui.dateEdit_dateBirth.setDate)
		#self.__character.dateBecomingChanged.connect(self.ui.dateEdit_dateBecoming.setDate)
		self.__character.dateGameChanged.connect(self.ui.dateEdit_dateGame.setDate)
		self.__character.ageChanged.connect(self.ui.label_age.setNum)
		#self.__character.ageBecomingChanged.connect(self.ui.label_ageBecoming.setNum)
		self.__character.virtueChanged.connect(self.updateVirtue)
		self.__character.viceChanged.connect(self.updateVice)
		self.__character.heightChanged.connect(self.ui.doubleSpinBox_height.setValue)
		self.__character.weightChanged.connect(self.ui.spinBox_weight.setValue)
		self.__character.eyesChanged.connect(self.ui.lineEdit_eyes.setText)
		self.__character.hairChanged.connect(self.ui.lineEdit_hair.setText)
		self.__character.nationalityChanged.connect(self.ui.lineEdit_nationality.setText)
		self.__character.pictureChanged.connect(self.updatePicture)
		self.__character.descriptionChanged.connect(self.ui.textEdit_description.setHtml)

		## Das Alter darf nie negativ werden können
		#self.ui.dateEdit_dateBirth.dateChanged.connect(self.ui.dateEdit_dateBecoming.setMinimumDate)
		self.ui.dateEdit_dateGame.dateChanged.connect(self.setMaxBirthday)

		## Ändert sich das Alter, gibt es andere Virtues und Vices.
		self.__character.ageChanged.connect(self.updateVirtueTitle)
		self.__character.ageChanged.connect(self.repopulateVirtues)
		self.__character.ageChanged.connect(self.updateViceTitle)
		self.__character.ageChanged.connect(self.repopulateVices)

		## Benachrichtigung bei Änderung der Alterskategorie.
		self.__character.ageChanged[str].connect(self.notifyOfAge)

		self.__character.ageChanged.connect(self.setHeightMinMax)
		self.__character.traits["Merit"]["Physical"]["Giant"].valueChanged.connect(self.updateHeight)
		self.__character.traits["Merit"]["Physical"]["GiantKid"].valueChanged.connect(self.updateHeight)
		self.__character.traits["Flaw"]["Physical"]["Dwarf"].valueChanged.connect(self.updateHeight)
		self.__character.traits["Merit"]["Physical"]["Tiny"].valueChanged.connect(self.updateHeight)



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

		cursor = self.ui.textEdit_description.textCursor()
		cursorPosition = cursor.position()

		self.__character.description = self.ui.textEdit_description.toHtml()

		cursor.setPosition(cursorPosition)
		self.ui.textEdit_description.setTextCursor(cursor)


	def updateButtonText( self ):
		"""
		Aktualisiert die Anzeige des Namens.
		"""

		nameStr = Identity.displayNameDisplay(self.__character.identity.surname, self.__character.identity.firstname, self.__character.identity.nickname)
		nameDisplay = nameStr
		if not nameStr:
			nameStr = self.tr("Name")
		self.ui.pushButton_name.setText( nameStr )
		for item in Config.GENDERS:
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


	def updateVirtueTitle( self, age ):
		"""
		Wenn die Alterskategorie sich ändert, ändert sich auch der Bezeichner für die Tugenden.
		"""

		label = self.tr("Virtue")
		if age < Config.AGE_ADULT:
			label = self.tr("Asset")
		if self.ui.label_virtue.text() != label:
			self.ui.label_virtue.setText( "{}:".format(label) )


	def updateViceTitle( self, age ):
		"""
		Wenn die Alterskategorie sich ändert, ändert sich auch der Bezeichner für die Laster.
		"""

		label = self.tr("Vice")
		if age < Config.AGE_ADULT:
			label = self.tr("Fault")
		if self.ui.label_vice.text() != label:
			self.ui.label_vice.setText( "{}:".format(label) )


	def repopulateVirtues(self, age):
		ageStr = Config.AGES[0]
		if age < Config.AGE_ADULT:
			ageStr = Config.AGES[1]

		virtueList = []
		for item in self.__storage.virtues:
			if item["age"] == ageStr:
				virtueList.append(item["name"])

		## Die Liste soll nur aktualisiert werden, wenn eine neue Alterskategorie erreicht wird.
		if self.ui.comboBox_virtue.itemText(0) not in virtueList:
			self.ui.comboBox_virtue.clear()
			self.ui.comboBox_virtue.addItems(virtueList)


	def repopulateVices(self, age):
		ageStr = Config.AGES[0]
		if age < Config.AGE_ADULT:
			ageStr = Config.AGES[1]

		viceList = []
		for item in self.__storage.vices:
			if item["age"] == ageStr:
				viceList.append(item["name"])

		## Die Liste soll nur aktualisiert werden, wenn eine neue Alterskategorie erreicht wird.
		if self.ui.comboBox_vice.itemText(0) not in viceList:
			self.ui.comboBox_vice.clear()
			self.ui.comboBox_vice.addItems(viceList)


	def openImage(self ):
		"""
		Öffnet einen Dialog zum Laden eines Charakterbildes und speichert selbiges im Charakter-Speicher.

		\note Das Bild wird auf eine in der Configurationsdatei festgelegte Maximalgröße skaliert, um die Größe überschaubar zu halten.
		"""

		appPath = PathTools.program_path()

		# Pfad zum Speicherverzeichnis
		savePath = ""
		if os.name == "nt":
			savePath = os.environ['HOMEPATH']
		else:
			savePath = os.environ['HOME']

		# Wenn Unterverzeichnis nicht existiert, suche im Programmverzeichnis.
		if ( not os.path.exists( savePath ) ):
			savePath = appPath

		fileData = QFileDialog.getOpenFileName(
			self,
			self.tr( "Select Image File" ),
			savePath,
			self.tr( "Images (*.jpg *.jpeg *.png *.bmp *.gif *.pgm *.pbm *.ppm *.svg )" )
		)

		# Sollte PySide verwendet werden!
		#filePath = fileData[0]
		# Sollte PyQt4 verwendet werden!
		filePath = fileData

		if ( filePath ):
			image = QPixmap(filePath)
			if image.width() > Config.CHARACTER_PIC_WIDTH_MAX or image.height() > Config.CHARACTER_PIC_HEIGHT_MAX:
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
			self.ui.pushButton_picture.setIcon(QIcon(image))
			self.ui.pushButton_pictureClear.setEnabled(True)


	def updateDateGame_era(self, era):
		"""
		Der Ära des Spiels verändert das maximale Datum des Spiels.
		"""

		if Config.era_auto_select:
			eraBeginDates = list( Config.ERAS.values() )
			eraBeginDates.sort()

			beginYear = Config.ERAS[era]
			endYear = QDate.currentDate()
			endYear = endYear.year()
			for year in eraBeginDates:
				if year > beginYear:
					endYear = year - 1
					break

			dateEraBegins = QDate(beginYear, 1, 1)
			dateEraEnds = QDate(endYear, 12, 31)

			eraModified = True
			newDate = None
			if self.ui.dateEdit_dateGame.date() < dateEraBegins:
				newDate = dateEraBegins
			elif self.ui.dateEdit_dateGame.date() > dateEraEnds:
				newDate = dateEraEnds
			else:
				eraModified = False

			if eraModified:
				self.ui.dateEdit_dateGame.setDate(newDate)
				text = self.tr("Date of game is set to {day}. {month}. {year} to be in the {era} era".format(day=newDate.day(), month=newDate.month(), year=newDate.year(), era=era))
				self.notificationSent.emit(text)
		else:
			self.__character.era = era


	def setCharacterEra(self, date):
		"""
		Der Ära des Spiels läßt sich entweder direkt einstellen, was die Zeit ändert oder über die Zeit.
		"""

		if Config.era_auto_select:
			eraBeginDates = list( Config.ERAS.values() )
			eraBeginDates.sort()

			#Debug.debug(eraBeginDates[::-1])

			beginYear = None
			for year in eraBeginDates[::-1]:
				if year <= date.year():
					beginYear = year
					break

			actualEra = None
			for era in Config.ERAS.items():
				if era[1] == beginYear:
					actualEra = era[0]

			if self.__character.era != actualEra:
				self.__character.era = actualEra
				text = self.tr("Era changed to {era}".format(era=era))
				self.notificationSent.emit(text)


	def setCharacterDateBirth(self, date):
		"""
		Speichert das Geburtsdatum des Charakters im Speicher.

		Allerdings muß zuvor möglicherweise um Erlaubnis gefragt werden.

		\todo Momentan wird keine Frage gestellt, da das nervt.
		"""

		#years = Calc.years(self.ui.dateEdit_dateBirth.date(), self.ui.dateEdit_dateGame.date())
		#if (self.__character.age < Config.AGE_ADULT <= years or years < Config.AGE_ADULT <= self.__character.age) and not self.warnAgeChange(years):
			#self.ui.dateEdit_dateBirth.setDate(self.__character.dateBirth)
		#else:
			#self.__character.setDateBirth(date)
		self.__character.setDateBirth(date)


	def notifyOfAge(self, age):
		text = self.tr("Character is an adult now (following the normal rules).")
		if age == "Kid":
			text = self.tr("Character is a kid now (following the rules for Innocents).")
		self.notificationSent.emit(text)


	def setCharacterDateGame(self, date):
		"""
		Speichert das Geburtsdatum des Charakters im Speicher.

		Allerdings muß zuvor möglicherweise um Erlaubnis gefragt werden.

		\todo Momentan wird keine Frage gestellt, da das nervt.
		"""

		#years = Calc.years(self.ui.dateEdit_dateBirth.date(), self.ui.dateEdit_dateGame.date())
		#if (self.__character.age < Config.AGE_ADULT <= years or years < Config.AGE_ADULT <= self.__character.age) and not self.warnAgeChange(years):
			#self.ui.dateEdit_dateGame.setDate(self.__character.dateGame)
		#else:
			#self.__character.setDateGame(date)
		self.__character.setDateGame(date)
		text = self.tr("Character is an adult now (following the normal rules).")
		if self.__character.age < Config.AGE_ADULT:
			text = self.tr("Character is a kid now (following the rules for Innocents).")
		self.notificationSent.emit(text)


	def setMaxBirthday(self):
		"""
		Ändert sich die Zeit im Spiel, ändert sich das maximal einzustellende Geburtsdatum, so daß der Charakter nicht jünger sein kann als der vorgegebene Minimalwert.
		"""

		maxDateBirth = self.ui.dateEdit_dateGame.date().addYears(-1 * Config.AGE_MIN)
		self.ui.dateEdit_dateBirth.setMaximumDate(maxDateBirth)
		## Damit auch im Charakter das Geburtsdatum geändert wird, immerhin wird nur das dateEdited-Signal ausgewertet...
		if maxDateBirth <= self.ui.dateEdit_dateBirth.date():
			self.__character.dateBirth = maxDateBirth


	#def warnAgeChange(self, newAge):
		#"""
		#Wird der Charakter vom Erwachsenen zum Kind (oder umgekehrt), sollte eine Bestätigung eingefordert werden.

		#Wird auf "No" geklickt, wird das Geburtsdatum wieder so verändert, daß das alte Alter beibehalten bleibt.
		#"""

		#text = self.tr("Your character is going to be an adult.")
		#if newAge < Config.AGE_ADULT:
			#text = self.tr("Your character is going to be a child.")
		#ret = QMessageBox.warning(
			#self,
			#self.tr( "Age category changed" ),
			#self.tr( "{} Do you want that to happen?".format(text) ),
			#QMessageBox.Yes | QMessageBox.No
		#)
		#if ret == QMessageBox.StandardButton.No:
			#return False
		#else:
			#return True


	def setHeightMinMax(self, age):
		self.ui.doubleSpinBox_height.setMinimum(Config.HEIGHT_MIN[Config.getAge(age)])
		self.ui.doubleSpinBox_height.setMaximum(Config.HEIGHT_MAX[Config.getAge(age)])


	def setCharacterHeight(self, height):
		"""
		Ändert sich die Körpergröße zu sehr, sollautomatisch der Merit Giant bzw. der Flaw Dwarf vorgeschlagen werden.

		\todo Bei Kindern heißt der Dwarf-Flaw "Tiny"
		"""

		ageText = Config.getAge(self.__character.age)

		giantTrait = self.__character.traits["Merit"]["Physical"]["Giant"]
		smallTrait = self.__character.traits["Flaw"]["Physical"]["Dwarf"]
		smallAddNotification = self.tr("Added the Dwarf Flaw.")
		smallRemoveNotification = self.tr("Removed the Dwarf Flaw.")
		if self.__character.age < Config.AGE_ADULT:
			giantTrait = self.__character.traits["Merit"]["Physical"]["GiantKid"]
			smallTrait = self.__character.traits["Merit"]["Physical"]["Tiny"]
			smallAddNotification = self.tr("Added the Tiny Merit.")
			smallRemoveNotification = self.tr("Removed the Tiny Merit.")

		if height >= Config.HEIGHT_GIANT_MIN[ageText]:
			if giantTrait.value > 0:
				pass
			elif self.warnHeightChange(height):
				giantTrait.value = 5
				self.notificationSent.emit(self.tr("Added the Giant Merit."))
			else:
				self.ui.doubleSpinBox_height.setValue(self.__character.height)
		elif height <= Config.HEIGHT_DWARF_MAX[ageText]:
			if smallTrait.value > 0:
				pass
			elif self.warnHeightChange(height):
				smallTrait.value = 2
				self.notificationSent.emit(smallAddNotification)
			else:
				self.ui.doubleSpinBox_height.setValue(self.__character.height)
		elif giantTrait.value:
			giantTrait.value = 0
			self.notificationSent.emit(self.tr("Removed the Giant Merit."))
		elif smallTrait.value:
			smallTrait.value = 0
			self.notificationSent.emit(smallRemoveNotification)

		self.__character.height = height


	def warnHeightChange(self, newHeight):
		"""
		Ändert sich die Körpergröße zu sehr, sollautomatisch der Merit Giant bzw. der Flaw Dwarf vorgeschlagen werden.
		"""

		## Wird der Charkater gerade geladen, werden keine Warnungen gezeigt und automatisch davon ausgegangen, daß der Anwender sie auch akzeptieren würde.
		if self.__character.isLoading:
			return True
		else:
			smallTrait = "Dwarf Flaw"
			if self.__character.age < Config.AGE_ADULT:
				smallTrait = "Tiny Merit"

			title = self.tr("Too big")
			text = self.tr("To be this big, the character needs to purchase the Giant Merit.")
			if newHeight <= Config.HEIGHT_DWARF_MAX[Config.getAge(self.__character.age)]:
				title = self.tr("Too small")
				text = self.tr("To be this small, the character needs to get the {}.".format(smallTrait))
			ret = QMessageBox.warning(
				self,
				title,
				self.tr( "{} Do you want that to happen?".format(text) ),
				QMessageBox.Yes | QMessageBox.No
			)
			if ret == QMessageBox.StandardButton.No:
				return False
			else:
				return True


	def updateHeight(self):
		"""
		Werden der Giant-Merit oder der Dwarf-Flaw verändert, muß die Körpergröße angepaßt werden.
		"""

		giantTrait = self.__character.traits["Merit"]["Physical"]["Giant"]
		smallTrait = self.__character.traits["Flaw"]["Physical"]["Dwarf"]
		if self.__character.age < Config.AGE_ADULT:
			giantTrait = self.__character.traits["Merit"]["Physical"]["GiantKid"]
			smallTrait = self.__character.traits["Merit"]["Physical"]["Tiny"]

		ageText = Config.getAge(self.__character.age)
		if giantTrait.value > 0 and self.ui.doubleSpinBox_height.value() < Config.HEIGHT_GIANT_MIN[ageText]:
			self.ui.doubleSpinBox_height.setValue(Config.HEIGHT_GIANT_MIN[ageText])
			self.notificationSent.emit(self.tr("Height changed to {} meters".format(Config.HEIGHT_GIANT_MIN[ageText])))
		elif giantTrait.value < 1 and self.ui.doubleSpinBox_height.value() >= Config.HEIGHT_GIANT_MIN[ageText]:
			newHeight = Config.HEIGHT_GIANT_MIN[ageText] - 0.01
			self.ui.doubleSpinBox_height.setValue(newHeight)
			self.notificationSent.emit(self.tr("Height changed to {} meters".format(newHeight)))
		elif smallTrait.value > 0 and self.ui.doubleSpinBox_height.value() > Config.HEIGHT_DWARF_MAX[ageText]:
			self.ui.doubleSpinBox_height.setValue(Config.HEIGHT_DWARF_MAX[ageText])
			self.notificationSent.emit(self.tr("Height changed to {} meters".format(Config.HEIGHT_DWARF_MAX[ageText])))
		elif smallTrait.value < 1 and self.ui.doubleSpinBox_height.value() <= Config.HEIGHT_DWARF_MAX[ageText]:
			newHeight = Config.HEIGHT_DWARF_MAX[ageText] + 0.01
			self.ui.doubleSpinBox_height.setValue(newHeight)
			self.notificationSent.emit(self.tr("Height changed to {} meters".format(newHeight)))
