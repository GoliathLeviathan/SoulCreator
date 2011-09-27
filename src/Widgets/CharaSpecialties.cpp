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

#include <QDebug>

#include "CharaSpecialties.h"


CharaSpecialties::CharaSpecialties( QWidget* parent ) : TraitSpecialties( parent ) {
	character = StorageCharacter::getInstance();

	connect( this, SIGNAL( checkedSpecialtiesChanged( QStringList ) ), this, SLOT( saveSpecialties( QStringList ) ) );
}

CharaSpecialties::~CharaSpecialties() {
}


void CharaSpecialties::saveSpecialties( QStringList list ) {
	QList< cv_TraitDetail > specialties;

	for ( int i = 0; i < list.count(); i++ ) {
		cv_TraitDetail detail;
		detail.name = list.at( i );
		specialties.append( detail );

// 		qDebug() << Q_FUNC_INFO << "Speichere" << specialties.at( i ).name << "von" << skill();
	}

	character->setSkillSpecialties( skill(), specialties );
}




