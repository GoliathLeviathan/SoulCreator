# -*- coding: utf-8 -*-

"""
\file
\author Victor von Rhein <victor@caern.de>

\section License

Copyright (C) 2011 by Victor von Rhein

This file is part of SoulCreator.

SoulCreator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SoulCreator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
"""




from __future__ import division, print_function

#from PySide.QtCore import Qt
#from PySide.QtGui import QDialog

##from src.Config import Config
#from src.Storage.StorageTemplate import StorageTemplate
#from src.Storage.StorageCharacter import StorageCharacter
#from src.Widgets.Components.CharaSpecies import CharaSpecies
#from src.Widgets.Dialogs.NameDialog import NameDialog




class cv_Name(object):
	"""
	@brief Diese Klasse speichert den vollständigen Namen eines Charakters.

	Jede Person besitzt eine Vielzahl von Namen, die über diese Klasse leicht zu verwalten sind.

	Bei Personen mit mehreren Identitäten, sollte eine Liste dieser Klasse angelegt werden, in welcher für jede Identität ein Eintrag vorgenommen wird. Auch ein Künstlername fällt unter diese Kategorie, solta also mit einem weiteren Listeneintrag realisiert werden.
	"""

	# Liste zur Speicherung von Namen.
	#
	# {
	# 	"forenames": [Name1, Name2, Name3, ...],
	# 	"surename": Name,
	# 	"honorname": Name,
	# 	"nickame": Name,
	# 	"supername": Name,
	# }
	# 
	# \sa firstName
	__name = {
		## Vorname.
		#
		# Dieser Name wurde dem Charakter von seinen Eltern gegeben. Es besteht die Möglichkeit, mehr als einen Vornamen zu besitzen, wesewegen diese Variable vom Typ StringList ist. Der erste Vorname in dieser Liste ist immer auch der Rufname.
		#
		# \sa self.firstName
		"forenames": [],
		## Nachname
		#
		# Der Familienname der Eltern.
		"surename": "",
		# Ein Beinahme, den der Charakter entweder durch ehrenvolle Taten, durch körperliche Besonderheiten oder durch Mißgeschick erworben hat.
		#
		# - der Starke
		# - die Schöne
		# - die Kleine
		# - der Treue
		"honorname": "",
		## Spitzname.
		#
		# Mit diesem Namen wird der Charakter meist von Freunden (Menschen) gerufen.
		"nickame": "",
		## Name unter den Übernatürlichen
		#
		# Dies ist der Name, der von den übrigen Kreaturen seiner Spezies verwendet wird.
		"supername": "",
	}
	

	def __init__( self, surename="", firstname="" ):
		self.__name["surename"] = surename
		self.__name["forenames"][0] = firstname


	def __getFirstName(self):
		"""
		Rufname
		
		Bei Personen mit nur einem Vornamen entspricht \ref firstName dem \ref foreName. Bei Personen mit mehreren Vornamen ist \ref firstName immer der allererste \ref foreName.
		"""
		
		return self.__name["forenames"][0]

	firstName = property(__getFirstName)


	def __getSureName(self):
		"""
		Nachname
		"""
		
		return self.__name["surename"]

	sureName = property(__getSureName)


	def __getRealName(self):
		"""
		Geburtsname.
		
		Dieser Name wurde dem Charakter von seinen Eltern gegeben und besteht aus Rufname (\ref firstName) und Nachname (\ref sureName) plus Namenszusatz (\ref affixName).
		
		\note Die Kenntnis dieses Namens erleichtert Magiern sympathische Magie.
		"""
		
		if (not self.firstName or not self.sureName):
			# In diesem Fall benötige ich keinen Abstand zwischen den Namen, da je einer leer ist.
			return "{}{}".format(firstName, sureName)
		else:
			return "{} {}".format(firstName, sureName)

	realName = property(__getRealName)


	@staticmethod
	def displayNameFull( last, fores ):
		"""
		Voller Name.
		
		Die Summe aller Namen wird formatiert und als ein einziger String ausgegeben.
		"""

		displayFull = ""

		if ( fores ):
			if type(fores) == list:
				displayFull = fores[0]
				for item in fores[1:]:
					displayFull += " {}".format(item)
			else:
				displayFull = fores

		# Vor dem Nachnamen nur dann ein Leerzeichen, wenn schon etwas davor steht.
		if ( displayFull ):
			displayFull += " "
		displayFull += last

		return displayFull


	@staticmethod
	def displayNameDisplay( last, first, nick ):
		"""
		Angezeigter Name.
		
		Dieser Name kann auf dem Charakterbogen angezeigt werden.
		"""
		
		displayDisplay = first
		if ( nick ):
			displayDisplay += " \"{}\"".format(nick)

		# Vor dem Nachnamen nur dann ein Leerzeichen, wenn schon etwas davor steht.
		if ( displayDisplay ):
			displayDisplay += " "
		displayDisplay += last

		return displayDisplay


	@staticmethod
	def displayNameHonor( first, honor ):
		"""
		Ehrenname
		"""
		
		displayHonor = first
		if ( honor ):
			displayHonor += " {}".format(honor)

		return displayHonor

