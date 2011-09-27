/**
 * \file
 * \author Victor von Rhein <goliath@caern.de>
 *
 * \section License
 *
 * Copyright (C) 2011 by Victor von Rhein
 *
 * This file is part of SoulCreator.
 *
 * SoulCreator is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SoulCreator is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef ATTRIBUTEWIDGET_H
#define ATTRIBUTEWIDGET_H

#include <QGridLayout>
#include <QLabel>

#include "Storage/StorageCharacter.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche Attribute angeordnet sind.
 *
 * Die Attribute werden in diesem Widget angeordnet.
 *
 * \todo Die Attribute in ein Gridlayout packen, damit bei den Werwölfen die Manipulation nicht so heraussticht.
 **/
class AttributeWidget : public QWidget {
		Q_OBJECT

	public:
		/**
		 * Konstruktor
		 **/
		AttributeWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~AttributeWidget();

	private:
		/**
		 * In diesem Layout werden die Attribute angeordnet.
		 **/
		QGridLayout *layout;
		StorageCharacter* character;
		/**
		 * Anzeige der Attributswerte für alle Formen eines Werwolfs.
		 **/
		QLabel *labelStr;
		QLabel *labelDex;
		QLabel *labelSta;
		QLabel *labelMan;

	public slots:

	private slots:
		/**
		 * Sorgt dafür, daß das Signal speciesChanged() mit dem richtigen Argument ausgesandt wird.
		 **/
		void emitSpeciesChanged(cv_Species::SpeciesFlag spe);
		/**
		 * Aktualisiert die Anzeige der unterschiedlichen Gestalten eines Werwolfs für die Stärke.
		 **/
		void updateshapeValuesStr(int val);
		/**
		 * Aktualisiert die Anzeige der unterschiedlichen Gestalten eines Werwolfs für die Geschicklichkeit.
		 **/
		void updateshapeValuesDex(int val);
		/**
		 * Aktualisiert die Anzeige der unterschiedlichen Gestalten eines Werwolfs für die Widerstandsfähigkeit.
		 **/
		void updateshapeValuesSta(int val);
		/**
		 * Aktualisiert die Anzeige der unterschiedlichen Gestalten eines Werwolfs für die Manipulation.
		 **/
		void updateshapeValuesMan(int val);

	signals:
		/**
		 * Sobald die Spezies verändert wird, wird dieses Signal ausgesandt.
		 **/
		void speciesChanged(bool sw /** Das Argument wird nur dann false, wenn die Spezies in cv_Species::Werewolf verändert wurde. */);
};

#endif
