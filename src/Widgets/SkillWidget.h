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
 * along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef SKILLWIDGET_H
#define SKILLWIDGET_H

#include <QGridLayout>

#include "../Datatypes/cv_TraitDetail.h"

#include <QWidget>


/**
 * @brief Das Widget, in welchem sämtliche Attribute angeordnet sind.
 *
 * Die Attribute werden in diesem Widget angeordnet.
 *
 * Wird bei irgendeiner Fertigkeit der Spazialisierungen-Knopf gedrückt, werden alle anderen Spezialisierungs-Knöpfe ausgeschalten.
 *
 * \todo Alles
 **/
class SkillWidget : public QWidget {
		Q_OBJECT

	public:
		SkillWidget( QWidget *parent = 0 );
		/**
		 * Zerstört das Objekt und gibt alle zugeteilten Ressourcen wieder frei.
		 **/
		~SkillWidget();

	private:
		QGridLayout *layout;

	public slots:

	private slots:
		/**
		 * Über diese Funktion werden alle anderen Spezialisierungs-Knöpfe deaktiviert, sobald einer aktiviert wird.
		 **/
		void toggleOffSpecialties(bool sw, QString skillName, QList< cv_TraitDetail > specialtyList);

	signals:
		void specialtiesClicked(bool sw, QString skillName, QList< cv_TraitDetail > specialtyList);
};

#endif
