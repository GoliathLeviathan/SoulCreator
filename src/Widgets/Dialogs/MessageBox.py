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

from PySide.QtCore import QObject
from PySide.QtGui import QMessageBox

from src.Config import Config
from src.Error import ErrXmlTooOldVersion




class MessageBox(QMessageBox):
	"""
	@brief Diese Klasse stellt verschiedene Standardnachrichtenfenster für das Programm dar.

	Über das Standardnachrichtenfenster können die Nachrichten über Ausnahmen bequem an den Nutzer weitergegeben werden. Unter anderem existiert auch eine Nachrichtenbox für die Ausnahmebehandlung.
	"""

	@staticmethod
	def exception(parent, message, description):
		"""
		Standardisierte Dialogbox für die Mitteilung einer Ausnahme an den Benutzer. Dient bislang Debug-Zwecken und sind noch keine normierten Fehlermeldungen.

		\todo Den Dialog so umwandeln, der er auch als Fehlermeldung einem Benutzer präsentiert werden kann und nicht nur als Debug-Hilfe dienen kann. Dies wird auch Änderungen in der \ref Exception -Klasse erfordern.
		"""
		
		obj = QObject()

		text = MessageBox.formatText(message, description)
		QMessageBox.critical(parent, obj.tr("Exception"), text)


#QMessageBox::StandardButton MessageBox::exception ( QWidget* parent, Exception error ) {
	"""
	Standardisierte Dialogbox für die Mitteilung einer Ausnahme an den Benutzer. Dient bislang Debug-Zwecken und sind noch keine normierten Fehlermeldungen.

	Dies ist eine überladene Methode der Funktion \ref MessageBox::exception( QWidget *parent, QString message, QString description ).
	"""
	
	#QString text = formatText(error.message(),  error.description());

	#critical ( parent, tr ( "Exception" ), text );
#}

#QMessageBox::StandardButton MessageBox::exception ( QWidget* parent ) {
	"""
	Standardisierte Dialogbox für die Mitteilung einer Ausnahme an den Benutzer. Dient bislang Debug-Zwecken und sind noch keine normierten Fehlermeldungen.
	
	Dies ist eine überladene Methode der Funktion \ref MessageBox::exception( QWidget *parent, QString message, QString description ).
	"""
	
	#QString text = formatText(tr ( "A problem occured." ),  tr ( "Cause or consequences of this problem are not known. Proceed on your own risk." ));

	#critical ( parent, tr ( "Exception" ), text );
#}

	@staticmethod
	def formatText ( message, description ):
		"""
		Formatiert Nachricht und Beschreibung für den Dialog.
		"""
		
		return MessageBox.formatMessage(message) + MessageBox.formatDescription(description)



	@staticmethod
	def formatMessage ( message ):
		"""
		Formatiert die wichtigen Nachrichten für den Dialog.
		"""
		
		importantText = "<p><span style='color:" + Config.importantTextColorName + "; font-size:large'>{}</span></p>".format(message)

		return importantText


	@staticmethod
	def formatDescription ( description ):
		"""
		Formatiert die ausfürhlichere Beschreibung für den Dialog.
		"""
		
		descriptionText = "<p>{}</p>".format(description)

		return descriptionText

