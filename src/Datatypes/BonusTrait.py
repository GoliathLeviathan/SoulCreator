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

#from src.Config import Config
from src.Datatypes.AbstractTrait import AbstractTrait
from src.Datatypes.StandardTrait import StandardTrait
from src.Debug import Debug
#from src.Error import ErrTraitType




class BonusTrait(StandardTrait):
	"""
	@brief Speichert zusätzlich noch den Bonuswert der Eigenschaft.
	"""


	bonusSpecialtiesChanged = Signal(object)
	totalvalueChanged = Signal(int)
	bonusValueChanged = Signal(object)


	def __init__(self, character, name="", value=0, parent=None):
		StandardTrait.__init__(self, character, name, value, parent)

		self.__bonusValue = 0
		self.__bonusSpecialties = []

		self.valueChanged.connect(self.emitTotalvalueChanged)
		self.bonusValueChanged.connect(self.emitTotalvalueChanged)


	@property
	def totalvalue(self):
		"""
		Der Eigenschaftswert mit Berücksichtigung des Bonuswertes.
		"""
		
		return self.value + self.bonusValue


	def emitTotalvalueChanged(self, value):
		self.totalvalueChanged.emit(self.totalvalue)


	def __getBonusValue(self):
		return self.__bonusValue

	def __setBonusValue(self, bonusValue):
		if self.__bonusValue != bonusValue:
			self.__bonusValue = bonusValue
			self.bonusValueChanged.emit(bonusValue)
			self.totalvalueChanged.emit(self.totalvalue)

	bonusValue = property(__getBonusValue, __setBonusValue)


	def __getBonusSpecialties(self):
		return self.__bonusSpecialties

	def __setBonusSpecialties(self, bonusSpecialties):
		if self.__bonusSpecialties != bonusSpecialties:
			self.__bonusSpecialties = bonusSpecialties
			self.bonusSpecialtiesChanged.emit(bonusSpecialties)
			self.traitChanged.emit(self)

	bonusSpecialties = property(__getBonusSpecialties, __setBonusSpecialties)

	def appendBonusSpecialty(self, name):
		"""
		Fügt der Liste von Bonusspezialisierungen eine hinzu.

		\note Diese Methode muß verwendet werden, wenn man das Signal \ref bonusSpecialtiesChanged nutzen möchte.
		"""

		self.__bonusSpecialties.append(name)
		self.bonusSpecialtiesChanged.emit(self.bonusSpecialties)
		self.traitChanged.emit(self)

	def removeBonusSpecialty(self, name):
		"""
		Entfernt eine Bonusspezialisierung.

		\note Diese Methode muß verwendet werden, wenn man das Signal \ref bonusSpecialtiesChanged nutzen möchte.
		"""

		self.__bonusSpecialties.remove(name)
		self.bonusSpecialtiesChanged.emit(self.bonusSpecialties)
		self.traitChanged.emit(self)


	def clearBonus(self):
		"""
		Entfernt alle Bonus-Werte dieser Eigenschaft.
		"""

		self.__bonusValue = 0
		self.__bonusSpecialties = []
		self.bonusValueChanged.emit(self.__bonusValue)
		self.bonusSpecialtiesChanged.emit(self.__bonusSpecialties)
		self.traitChanged.emit(self)
