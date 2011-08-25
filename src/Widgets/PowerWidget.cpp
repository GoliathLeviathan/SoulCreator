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

#include <QGridLayout>
#include <QDebug>

#include "CharaTrait.h"
#include "../Datatypes/cv_Trait.h"
#include "../Exceptions/Exception.h"
#include "../Config/Config.h"
#include "../Storage/StorageTemplate.h"
#include "../CMakeConfig.h"

#include "PowerWidget.h"


PowerWidget::PowerWidget( QWidget *parent ) : QWidget( parent )  {
	QVBoxLayout* layoutTop = new QVBoxLayout( this );
	setLayout( layoutTop );

	this->setMaximumHeight(150);

	scrollArea = new QScrollArea( this );
	scrollArea->setSizePolicy( QSizePolicy::MinimumExpanding, QSizePolicy::Minimum );
	scrollArea->setWidgetResizable( true );
	scrollArea->setFrameStyle( 0 );

	layoutTop->addWidget( scrollArea );

	QWidget* widget = new QWidget();
	widget->setSizePolicy( QSizePolicy::Preferred, QSizePolicy::Minimum );

	QVBoxLayout* layoutPower = new QVBoxLayout();
	widget->setLayout( layoutPower );

	scrollArea->setWidget( widget );
	widget->show();

	StorageTemplate storage;

	cv_Trait::Type type = cv_Trait::Power;

	QList< cv_Trait::Category > categories;
	categories.append( cv_Trait::CategoryNo );

	QList< cv_Trait > list;

	// Powers werden in einer Spalte heruntergeschrieben.
	for ( int i = 0; i < categories.count(); i++ ) {
		list = storage.powers( categories.at( i ) );

		for ( int j = 0; j < list.count(); j++ ) {
// 			qDebug() << Q_FUNC_INFO << "Zähle Kräfte" << j;
			for ( int k = 0; k < Config::traitMultipleMax; k++ ) {
				CharaTrait *charaTrait = new CharaTrait( this, list.at( j ) );
				// Wert definitiv ändern, damit alle Werte in den Charakter-Speicher übernommen werden.
				charaTrait->setValue( 5 );
				charaTrait->setValue( 0 );
				layoutPower->addWidget( charaTrait );

				// Eigenschaften mit Beschreibungstext werden mehrfach dargestellt, da man sie ja auch mehrfach erwerben kann. Alle anderen aber immer nur einmal.
				if ( !list.at( j ).custom ) {
					break;
				}
			}
		}
	}
}

PowerWidget::~PowerWidget() {
	delete scrollArea;
}



