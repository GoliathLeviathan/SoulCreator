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

#ifndef CV_NAMELIST_H
#define CV_NAMELIST_H

#include <QString>

#include "cv_Identity.h"

#include <QList>

/**
 * @brief In dieser Klasse werden sämtliche Identitäten eines Charakters gespeichert.
 *
 * Ein Charkater mit mehreren (möglicherweise flaschen) Identitäten und Künstlernamen benötigt für jede Identität einen eigenen Namenseintrag, der wieder aus einer komplexen Zusammensetzung anderer Namen Besteht.
 *
 * Diese Klasse stellt eine Liste aller Namen für jede einzelne Identität eines Charakters zusammen. Dabei steht der echte Name immer an erster Stelle dieser Liste. Dies ist wirchtig für den "echten Namen", der von Magier benötigt wird, um ihnen die sympathische Magie zu erleichtern.
 **/
class cv_IdentityList : public QList< cv_Identity > {
	public:
		/**
		 * Konstruktor, bei dem die Namenseinträge direkt angegeben werden können.
		 **/
		cv_IdentityList( QString sureName = "", QString firstName = "" );
		
		/**
		 * Dies ist der echte Name einer Person. Der Name, der für Magier so wertvoll ist, um eine sympathische Verbindung leichter herstellen zu können.
		 **/
		QString realName() const;

		void reset();
};

#endif

