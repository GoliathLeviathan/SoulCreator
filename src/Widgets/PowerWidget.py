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




#from PyQt4.QtCore import pyqtSignal as Signal
#from PyQt4.QtCore import Qt
#from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBox

#import src.Config as Config
#from src import Error
from src.Widgets.CategoryWidget import CategoryWidget
#import src.Debug as Debug




class PowerWidget(CategoryWidget):
	"""
	@brief Das Widget, in welchem sämtliche Übernatürlichen Kräfte angeordnet sind.

	Hier tauchen die nur die übergeordneten Powers auf, in dem anderen Widget dann die speziellen Kräfte (Vampire-Rituale, Werwolf-Gaben + Rituale, Mage-Rotes, Changeling-???)
	"""


	def __init__(self, template, character, parent=None):
		super(PowerWidget, self).__init__(template, character, typ="Power", isCheckable=False, parent=parent)



