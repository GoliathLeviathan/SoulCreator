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




from PyQt4.QtCore import pyqtSignal as Signal
#from PyQt4.QtGui import QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel

#import src.Config as Config
from src.Widgets.Components.TraitLine import TraitLine
from src.Datatypes.BonusTrait import BonusTrait
#import src.Debug as Debug




class CharaTrait(TraitLine):
	"""
	\brief Mit den gespeicherten Werten vernetzte Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.

	Anders als \ref TraitLine, ist dieses Widget direkt mit der korrespondierenden Eigenschaft in der Klasse \ref StorageCharacter verknüpft. Ändert sich der Wert dort, wird automatisch dieses Widget entsprechend verändert. Gleichermaßen wird \ref StorageCharacter verändert, sollte der Benutzer dieses Widget ändern.

	\todo Solange kein Text in der Textbox einer Eigenschaft mit Zusatztext steht, sollte der Wert nicht verändert werden können.
	"""


	specialtiesClicked = Signal(bool, object)
	visibilityChanged = Signal(bool)


	def __init__(self, trait, parent=None):
		super(CharaTrait, self).__init__(trait.name, trait.value, parent)

		self.__trait = trait

		# Falls ich mit der Maus den Wert ändere, muß er auch entsprechend verändert werden.
		self.valueChanged.connect(self.setTraitValue)
		self.textChanged.connect(self.setTraitCustomText)
		#connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideSpecialtyWidget( cv_AbstractTrait::Type ) ) );
		#connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideDescriptionWidget() ) );
		#connect( this, SIGNAL( specialtiesClicked( bool ) ), this, SLOT( emitSpecialtiesClicked( bool ) ) );
		self.buttonToggled.connect(self.emitSpecialtiesClicked)

		#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideTraitIfNotAvailable( cv_Species::SpeciesFlag ) ) );
		self.__trait.valueChanged.connect(self.setValue)
		if type(self.__trait) == BonusTrait:
			self.__trait.bonusValueChanged.connect(self.setBonusValue)
		self.__trait.customTextChanged.connect(self.setText)
		self.__trait.specialtiesChanged.connect(self.setSpecialtiesButtonText)

		#// Die Signale hier zu verbinden funktioniert offensichtlich nicht. Vielleicht weil einige Fertigkeiten dann noch nicht existieren.
		#connect( traitPtr(), SIGNAL( availabilityChanged(bool)), this, SLOT( setEnabled(bool)) );
		self.__trait.availableChanged.connect(self.setEnabled)


	def setTraitValue( self, value ):
		"""
		Wenn der Wert dieses Widgets verändert wird, muß auch der dadurch repräsentierte Wert im Speicher verändert werden. Dies geschieht über diesen Slot.
		"""

		#Debug.debug("Eigenschaft {} erhält den Wert {}".format(self.__trait["name"], value))
		if self.__trait.value != value:
			self.__trait.value = value
		#Debug.debug("Eigenschaft {} hat den Wert {}".format(self.__trait["name"], self.__trait["value"]))


	#def __getCustomText() const {
		#return traitPtr()->customText();
	#}
	def setTraitCustomText( self, text ):
		"""
		Legt den Zusatztext fest.

		Dabei wird automatisch der Wert im Speicher aktualisiert und natürlich auch die Anzeige des Widget.
		"""

		if self.__trait.customText != text:
			self.__trait.customText = text

			#emit traitChanged( traitPtr() );


	def emitSpecialtiesClicked(self, sw):
		self.specialtiesClicked.emit(sw, self.__trait)


	def hideOrShowTrait(self, species=None, age=None, era=None, breed=None, faction=None):
		"""
		Versteckt oder zeigt diese Eigenschaft.
		"""

		visible = True
		# Es können nur Eigenschaften versteckt werden, die einen age- bzw. era-Eintrag besitzen.
		if (
			(species and self.__trait.species and self.__trait.species != species) or
			(age and self.__trait.age and self.__trait.age != age) or
			(era and self.__trait.era and era not in self.__trait.era) or
			((breed or faction) and self.__trait.only and breed not in self.__trait.only and faction not in self.__trait.only)
		):
			visible = False

		self.setVisible(visible)
		self.visibilityChanged.emit(visible)


	def setSpecialtiesButtonText(self, specialties):
		#count = len(self.__trait.specialties)
		count = len(specialties)
		self.buttonText = count