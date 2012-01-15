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

from PySide.QtCore import QObject, Signal
#from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QButtonGroup

from src.Config import Config
#from src import Error
#from ReadXml import ReadXml
#from src.Widgets.Components.CharaTrait import CharaTrait
from src.Debug import Debug




class CalcAdvantages(QObject):
	"""
	\brief Diese Klasse führt die berechnung der abgeleiteten Eigenschaften durch.

	Die hier deklarierten Berechnungsfunktionen werden zwar bei der Änderung jeder Eigenschaft aufgerufen, aber berechnen die Werte nur, wenn eine Eigenschaft verändert wurde, welche Einfluß auf das Ergebnis nimmt. Sie geben allerdings immer das Ergebnis der berechnung aus. Entweder den neuen Wert, oder den alten Wert, der in dieser Klasse gespeichert wird.
	"""


	sizeChanged = Signal(int)
	initiativeChanged = Signal(int)
	speedChanged = Signal(int)
	defenseChanged = Signal(int)
	healthChanged = Signal(int)
	willpowerChanged = Signal(int)


	def __init__(self, character, parent=None):
		QObject.__init__(self, parent)

		self.__character = character

		self.__size = 0
		self.__initiative = 0
		self.__speed = 0
		self.__defense = 0
		self.__health = 0
		self.__willpower = 0

		self.__attrWit = self.__character.traits["Attribute"]["Mental"]["Wits"]
		self.__attrRes = self.__character.traits["Attribute"]["Mental"]["Resolve"]
		self.__attrStr = self.__character.traits["Attribute"]["Physical"]["Strength"]
		self.__attrDex = self.__character.traits["Attribute"]["Physical"]["Dexterity"]
		self.__attrSta = self.__character.traits["Attribute"]["Physical"]["Stamina"]
		self.__attrCom = self.__character.traits["Attribute"]["Social"]["Composure"]
		self.__meritGiant = self.__character.traits["Merit"]["Physical"]["Giant"]
		self.__meritFleetOfFoot = self.__character.traits["Merit"]["Physical"]["Fleet of Foot"]
		self.__meritFastReflexes = self.__character.traits["Merit"]["Physical"]["Fast Reflexes"]

		self.sizeChanged.connect(self.calcHealth)


	#@property
	#def size(self):
		#return self.__size


	#@property
	#def initiative(self):
		#return self.__initiative


	#@property
	#def speed(self):
		#return self.__speed


	#@property
	#def defense(self):
		#"""
		#Gibt die berechnete Defense des Charakters aus.
		#"""

		#return self.__defense


	#@property
	#def health(self):
		#"""
		#Gibt die berechnete Gesundheit des Charakters aus.
		#"""

		#return self.__health


	#@property
	#def willpower(self):
		#"""
		#Gibt die berechnete Willenskraft des Charakters aus.
		#"""

		#return self.__willpower


	def calcSize(self):
		"""
		Berechnung der Größe des Charakters.
		"""

		result = 5
		if self.__character.age < Config.adultAge:
			result -= 1

		if ( self.__meritGiant.value > 0 ):
			result += 1

		if ( self.__size != result ):
			self.__size = result
			self.sizeChanged.emit( result )

		return self.__size


	def calcInitiative(self):
		"""
		Berechnung der Initiative des Charakters.

		\todo Bislang nur von Dexterity, Composure und Fast Reflexes abhängig. Möglicherweise vorhandene Übernatürliche Eigenschaften werden nicht berücksichtigt.
		"""

		result = self.__attrDex.value + self.__attrCom.value + self.__meritFastReflexes.value

		if ( self.__initiative != result ):
			self.__initiative = result
			self.initiativeChanged.emit( result )

		return self.__initiative


	def calcSpeed(self):
		"""
		Berechnung der Geschwindigkeit des Charakters.

		\todo Bislang nur von Strength und Dexterity abhängig. Möglicherweise vorhandene Übernatürliche Eigenschaften werden nicht berücksichtigt.
		"""

		result = self.__attrStr.value + self.__attrDex.value + 5 + self.__meritFleetOfFoot.value;

		if ( self.__speed != result ):
			self.__speed = result
			self.speedChanged.emit( result )

		return self.__speed


	def calcDefense(self):
		"""
		Berechnung der Defense

		\todo Bislang nicht von der Spezies abhängig: Tiere sollten stets das größere von Dex und Wits als Defense haben.
		"""

		result = min( self.__attrWit.value, self.__attrDex.value )

		if ( self.__defense != result ):
			self.__defense = result
			self.defenseChanged.emit( result )

		return self.__defense


	def calcHealth(self):
		"""
		Berechnung der Gesundheit.
		"""

		## Bevor ich die Gesundheit ausrechnen kann, muß erst die Größe feststehen.
		size = self.calcSize()

		result = self.__attrSta.value + size

		#Debug.debug("Berechne {} + {} = {}".format(self.__attrSta.value, size, result))

		if ( self.__health != result ):
			self.__health = result
			self.healthChanged.emit( result )

		return self.__health


	def calcWillpower(self):
		"""
		Berechnung der Willenskraft.
		"""

		result = self.__attrRes.value + self.__attrCom.value

		if ( self.__willpower != result ):
			self.__willpower = result
			self.willpowerChanged.emit( result )

		return self.__willpower


