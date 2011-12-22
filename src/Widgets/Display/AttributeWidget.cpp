/**
 * \file
 * \author Victor von Rhein <victor@caern.de>
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

// #include <QHBoxLayout>
#include <QVBoxLayout>
#include <QGroupBox>
#include <QRadioButton>
// #include <QStringList>
#include <QDebug>

#include "Widgets/Components/CharaTrait.h"
#include "Calc/CalcAdvantages.h"
#include "Datatypes/Traits/AttributeTrait.h"
// #include "Datatypes/cv_Shape.h"
// #include "Exceptions/Exception.h"
// #include "Config/Config.h"
// #include "Storage/StorageTemplate.h"
#include "Widgets/Dialogs/MessageBox.h"

#include "AttributeWidget.h"


AttributeWidget::AttributeWidget( QWidget *parent ) : QWidget( parent )  {
	character = StorageCharacter::getInstance();

	layout = new QVBoxLayout( this );
	setLayout( layout );

	layoutAttributes = new QGridLayout();
	layout->addLayout( layoutAttributes );

// 	QFrame* frame = new QFrame( this );
// 	layout->addWidget( frame );
//
// 	QVBoxLayout* layoutHeader = new QVBoxLayout();
// 	frame->setLayout( layoutHeader );
//
	QLabel* labelPower = new QLabel( "<b>" + tr( "Power" ) + "</b>" );
	labelPower->setAlignment( Qt::AlignRight );

	QLabel* labelFinesse = new QLabel( "<b>" + tr( "Finesse" ) + "</b>" );
	labelFinesse->setAlignment( Qt::AlignRight );

	QLabel* labelResistance = new QLabel( "<b>" + tr( "Resistance" ) + "</b>" );
	labelResistance->setAlignment( Qt::AlignRight );

	int actualRow = 1;
	int actualColumn = 0;

	layoutAttributes->addWidget( labelPower, actualRow, actualColumn );
	actualRow++;
	layoutAttributes->addWidget( labelFinesse, actualRow, actualColumn );
	actualRow++;
	layoutAttributes->addWidget( labelResistance, actualRow, actualColumn );

	storage = new StorageTemplate( this );

	cv_AbstractTrait::Type type = cv_AbstractTrait::Attribute;

	QList< cv_AbstractTrait::Category > categoryList = cv_AbstractTrait::getCategoryList( type );

	QList< Trait* > list;

	labelStr = new QLabel( this );
	labelDex = new QLabel( this );
	labelSta = new QLabel( this );
	labelMan = new QLabel( this );

	connect( this, SIGNAL( speciesChanged( bool ) ), labelStr, SLOT( setHidden( bool ) ) );
	connect( this, SIGNAL( speciesChanged( bool ) ), labelDex, SLOT( setHidden( bool ) ) );
	connect( this, SIGNAL( speciesChanged( bool ) ), labelSta, SLOT( setHidden( bool ) ) );
	connect( this, SIGNAL( speciesChanged( bool ) ), labelMan, SLOT( setHidden( bool ) ) );

	for ( int i = 0; i < categoryList.count(); ++i ) {
		try {
			list = storage->traits( type, categoryList.at( i ) );
		} catch ( eTraitNotExisting &e ) {
			MessageBox::exception( this, e.message(), e.description() );
		}

		// Zeichnen des Separators zwischen den einzelnen Kategorien
		actualColumn++;

		QFrame* vLine = new QFrame( this );
		vLine->setFrameStyle( QFrame::VLine );
		layoutAttributes->addWidget( vLine, 1, actualColumn, list.count(), 1, Qt::AlignHCenter );

// 		layout->setColumnMinimumWidth(actualColumn, Config::traitCategorySpace);
		layoutAttributes->setColumnStretch( actualColumn, 1 );

		// Jetzt sind wir in der Spalte für die tatsächlchen Attribute
		actualColumn++;

		// Aber zuerst kommt die Überschrift für die einzelnen Kategorien.
		QLabel* header = new QLabel();
		header->setAlignment( Qt::AlignHCenter );
		header->setText( "<b>" + cv_AbstractTrait::toString( categoryList.at( i ) ) + "</b>" );
		layoutAttributes->addWidget( header, 0, actualColumn );

		// Einfügen der tatsächlichen Attribute
		for ( int j = 0; j < list.count(); ++j ) {
			// Anlegen der Eigenschaft im Speicher
			Trait* traitPtr = character->addTrait( list[j] );

			// Anlegen des Widgets, das diese Eigenschaft repräsentiert.
			CharaTrait* trait = new CharaTrait( this, traitPtr, list[j] );
			trait->setValue( 1 );

			layoutAttributes->addWidget( trait, j + 1, actualColumn );

			if ( trait->category() == cv_AbstractTrait::Physical ) {
				if ( trait->name() == "Strength" ) {
					layoutAttributes->addWidget( labelStr, j + 1, actualColumn + 1 );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesStr( int ) ) );
				} else if ( trait->name() == "Dexterity" ) {
					layoutAttributes->addWidget( labelDex, j + 1, actualColumn + 1 );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesDex( int ) ) );
				} else if ( trait->name() == "Stamina" ) {
					layoutAttributes->addWidget( labelSta, j + 1, actualColumn + 1 );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesSta( int ) ) );
				}
			} else if ( trait->category() == cv_AbstractTrait::Social ) {
				if ( trait->name() == "Manipulation" ) {
					layoutAttributes->addWidget( labelMan, j + 1, actualColumn + 1 );
					connect( trait, SIGNAL( valueChanged( int ) ), this, SLOT( updateshapeValuesMan( int ) ) );
				}
			}
		}

		// Bei Werwölfen erscheint hier Zusatztext. Und damit der Sparator richtig gesetzt wird, muß die aktuelle Spalte ein weitergezählt werden.
		actualColumn++;
	}

	layout->addSpacing( Config::vSpace );

	QGridLayout* layoutBonus = new QGridLayout();
	layout->addLayout( layoutBonus );

	QLabel* labelBonus = new QLabel( this );
	labelBonus->setText( tr( "Bonus Attribute:" ) );

	layoutButtonsBonus = new QVBoxLayout();

	buttonsBonus = new QButtonGroup( this );

	layoutBonus->addWidget( labelBonus, 0, 0, Qt::AlignTop | Qt::AlignLeft );
	layoutBonus->addLayout( layoutButtonsBonus, 0, 1 );
// 	layoutBonus->addItem(new QSpacerItem(0,0), 0, 2);
	layoutBonus->addWidget( new QWidget( this ), 0, 2 );
	layoutBonus->setColumnStretch( 2, 1 );

	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( filterBonusAttribute() ) );
	connect( character, SIGNAL( breedChanged( QString ) ), this, SLOT( filterBonusAttribute() ) );
	connect( buttonsBonus, SIGNAL( buttonClicked( int ) ), this, SLOT( addAttributeBonus( int ) ) );
	connect( character, SIGNAL( speciesChanged( cv_Species::SpeciesFlag ) ), this, SLOT( emitSpeciesChanged( cv_Species::SpeciesFlag ) ) );
}

AttributeWidget::~AttributeWidget() {
	delete buttonsBonus;
	delete layoutButtonsBonus;
	delete storage;
	delete labelMan;
	delete labelStr;
	delete labelDex;
	delete labelSta;
	delete layoutAttributes;
}


void AttributeWidget::updateshapeValuesStr( int val ) {
	QStringList txt;

	// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		txt.append( QString::number( CalcAdvantages::strength( val, cv_Shape::getShapeList().at( i ) ) ) );
	}

	labelStr->setText( txt.join( "/" ) );
}

void AttributeWidget::updateshapeValuesDex( int val ) {
	QStringList txt;

	// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		txt.append( QString::number( CalcAdvantages::dexterity( val, cv_Shape::getShapeList().at( i ) ) ) );
	}

	labelDex->setText( txt.join( "/" ) );
}

void AttributeWidget::updateshapeValuesSta( int val ) {
	QStringList txt;

	// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		txt.append( QString::number( CalcAdvantages::stamina( val, cv_Shape::getShapeList().at( i ) ) ) );
	}

	labelSta->setText( txt.join( "/" ) );
}

void AttributeWidget::updateshapeValuesMan( int val ) {
	QStringList txt;

	// Die Hishu-Gestalt interessiert nicht, da diese ja direkt eingegeben wird.

	for ( int i = 1; i < cv_Shape::getShapeList().count(); ++i ) {
		txt.append( QString::number( CalcAdvantages::manipulation( val, cv_Shape::getShapeList().at( i ) ) ) );
	}

	labelMan->setText( txt.join( "/" ) );
}

void AttributeWidget::emitSpeciesChanged( cv_Species::SpeciesFlag spe ) {
	if ( spe == cv_Species::Werewolf ) {
		emit speciesChanged( false );
	} else {
		emit speciesChanged( true );
	}
}


void AttributeWidget::filterBonusAttribute() {
	cv_AbstractTrait::Type type = cv_AbstractTrait::Attribute;

	QList< TraitBonus* > listBonus = storage->traitsBonus( type, character->species() );

	// Bereits platzierte Knöpfe löschen, bevor wir sie wieder neu einfügen.
	int listCount = buttonsBonus->buttons().count();
	for ( int i = listCount; i > 0; --i ) {

		delete buttonsBonus->buttons().at( i - 1 );
	}

	for ( int i = 0; i < listBonus.count(); ++i ) {
		if ( listBonus.at( i )->breedDependant() == character->breed() ) {
			// Füge neue Knöpfe hinzu
			QRadioButton* button = new QRadioButton( listBonus.at( i )->name() );
			buttonsBonus->addButton( button );
			layoutButtonsBonus->addWidget( button );

			if ( i == 0 ) {
				button->click();
			}
		}
	}
}


void AttributeWidget::addAttributeBonus( int id ) {
	QList< Trait* > list = character->traits( cv_AbstractTrait::Attribute );

	for ( int i = 0; i < list.count(); ++i ) {
		list.at( i )->setBonus( false );

// 		qDebug() << Q_FUNC_INFO << buttonsBonus->button( id )->text();
		if ( buttonsBonus->button( id )->text() == list.at( i )->name() ) {
			list.at( i )->setBonus( true );
// 			qDebug() << Q_FUNC_INFO << "Lege Bonuseigenschaft von" << list.at(i)->name() << "auf" << list.at(i)->isBonus();
		}
	}
}