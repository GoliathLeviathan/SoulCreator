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

from PySide.QtCore import Signal

from src.Config import Config
from src.Widgets.Components.TraitLine import TraitLine
from src.Debug import Debug




class CharaTrait(TraitLine):
	"""
	\brief Mit den gespeicherten Werten vernetzte Darstellung einer einzigen Eigenschaft auf dem Charakterbogen.
 
	Anders als \ref TraitLine, ist dieses Widget direkt mit der korrespondierenden Eigenschaft in der Klasse \ref StorageCharacter verknüpft. Ändert sich der Wert dort, wird automatisch dieses Widget entsprechend verändert. Gleichermaßen wird \ref StorageCharacter verändert, sollte der Benutzer dieses Widget ändern.
 
	\todo Solange kein Text in der TExtbox einer Eigenschaft mit Zusatztext steht, sollte der Wert nicht verändert werden können.
 
	\todo Den Parser \ref StringBoolParser erweitern, damit übriggebliebener Text nach den Ersetzungen der Eigesncahften durch ihre Werte mit 0 gleichgesetzt wird. Aktuell mache ich das durch Stringmanipulation, aber das ist natürlich langsamer.
 
	\todo eine fast identische Klasse schaffen, welche Trait anstelle von cv_Trait nutzt und direkte Siganel empfangen kann.
	"""


	specialtiesClicked = Signal(bool, object)


	def __init__(self, trait, parent=None):
		TraitLine.__init__(self, trait.name, trait.value, parent)

		self.__trait = trait

		# Falls ich mit der Maus den Wert ändere, muß er auch entsprechend verändert werden.
		self.valueChanged.connect(self.setTraitValue)
		#connect( this, SIGNAL( textChanged( QString ) ), this, SLOT( setCustomText( QString ) ) );
		#connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideSpecialtyWidget( cv_AbstractTrait::Type ) ) );
		#connect( this, SIGNAL( typeChanged( cv_AbstractTrait::Type ) ), this, SLOT( hideDescriptionWidget() ) );
		#connect( this, SIGNAL( specialtiesClicked( bool ) ), this, SLOT( emitSpecialtiesClicked( bool ) ) );
		self.buttonClicked.connect(self.emitSpecialtiesClicked)
		#self.__trait.specialtiesChanged.connect(self.uncheckButton)

		#connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( hideTraitIfNotAvailable( cv_Species::SpeciesFlag ) ) );
		self.__trait.valueChanged.connect(self.setValue)

		#// Die Signale hier zu verbinden funktioniert offensichtlich nicht. Vielleicht weil einige Fertigkeiten dann noch nicht existieren.
		#connect( traitPtr(), SIGNAL( availabilityChanged(bool)), this, SLOT( setEnabled(bool)) );

		#if ( !traitPtr()->possibleValues().isEmpty() ) {
			#setPossibleValues( traitPtr()->possibleValues() );
		#}

		#hideSpecialtyWidget( trait->type() );
		#hideDescriptionWidget();


#Trait* CharaTrait::traitPtr() const {
	#return ptr_trait;
#}

#void CharaTrait::setTraitPtr( Trait* trait ) {
	#if ( ptr_trait != trait ) {
		#ptr_trait = trait;
	#}
#}


#// int CharaTrait2::value() const {
#// 	return traitPtr()->value();
#// }
#// void CharaTrait2::setValue( int val ) {
#// 	qDebug() << Q_FUNC_INFO << name() << val << value();
#// 	if ( value() != val ) {
#// 		TraitLine::setValue( val );
#// 	}
#// }

	def setTraitValue( self, value ):
		"""
		Wenn der Wert dieses Widgets verändert wird, muß auch der dadurch repräsentierte Wert im Speicher verändert werden. Dies geschieht über diesen Slot.
		"""
		
		#Debug.debug("Eigenschaft {} erhält den Wert {}".format(self.__trait["name"], value))
		if self.__trait.value != value:
			self.__trait.value = value
		#Debug.debug("Eigenschaft {} hat den Wert {}".format(self.__trait["name"], self.__trait["value"]))


#QString CharaTrait::customText() const {
	#return traitPtr()->customText();
#}
#void CharaTrait::setCustomText( QString txt ) {
	"""
	Legt den Zusatztext fest.
	
	Dabei wird automatisch der Wert im Speicher aktualisiert und natürlich auch die Anzeige des Widget.
	"""
	
	#if ( traitPtr()->customText() != txt ) {
		#traitPtr()->setCustomText( txt );

		#TraitLine::setText( txt );

		#emit traitChanged( traitPtr() );
	#}
#}




#bool CharaTrait::custom() const {
	#return ptr_trait->custom();
#}

#void CharaTrait::setCustom( bool sw ) {
	#"""
	#Legt fest, ob es sich um eine Eigenschaft mit einem erklärenden Text handelt.
	#"""
	
	#if ( ptr_trait->custom() != sw ) {
		#ptr_trait->setCustom( sw );

		#emit traitChanged( traitPtr() );
	#}
#}


	def emitSpecialtiesClicked(self, sw):
		self.specialtiesClicked.emit(sw, self.__trait)


	#def uncheckButton( self ):
		##Debug.debug("Alle Spezialisierungsknöpfe werden wieder deaktiviert")
		#self.setSpecialtyButtonChecked(False)



#void CharaTrait::hideTraitIfNotAvailable( cv_Species::SpeciesFlag sp ) {
	#"""
	#Kontrolliert, ob die Eigenschaft für die Spezies im Argument überhaupt existiert.
	
	#Wenn nicht, werde sie versteckt und auf 0 gesetzt.
	#"""
	
	#if ( species().testFlag( sp ) ) {
		#setHidden( false );
	#} else {
		#setValue( 0 );
		#setHidden( true );
	#}
#}


	def hideOrShowTrait(self, reason):
		"""
		Versteckt oder zeigt diese Eigenschaft, weil reason eingetreten ist.
		"""

		#Debug.debug("Eigenschaft {} wegen {}".format(self.name, reason))
		#Debug.debug(self.__trait.age)
		if type(reason) == int:
			if self.__trait.age == Config.ages[0]:
				if reason < Config.adultAge:
					self.setHidden(False)
				else:
					self.setHidden(True)
					Debug.debug("Verstecke {}, da Alter {}".format(self.name, reason))
			elif self.__trait.age == Config.ages[1]:
				if reason < Config.adultAge:
					self.setHidden(True)
					Debug.debug("Verstecke {}, da Alter {}".format(self.name, reason))
				else:
					self.setHidden(False)
		if type(reason) in [str, unicode]:
			Debug.debug(self.__trait.era)
			if self.__trait.era and self.__trait.era != reason:
				self.setHidden(True)
				Debug.debug("Verstecke {}, da Ära {}".format(self.name, reason))
			else:
				self.setHidden(False)

