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


// #include "Exceptions/Exception.h"

#include "cv_Derangement.h"


cv_Derangement::cv_Derangement( QString txt, int mor, cv_Species::Species spe, cv_AbstractTrait::Category ca ) : cv_AbstractTrait( txt, spe, cv_AbstractTrait::Derangement, ca ) {
	v_morality = mor;
}

int cv_Derangement::morality() const
{
	return v_morality;
}
void cv_Derangement::setMorality( int val )
{
	v_morality = val;
}
