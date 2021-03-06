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




import sys




_WARNING_PREFIX = "WARNING"


def print_warning( *args ):
	"""
	Print warning message on console.
	"""

	print( _WARNING_PREFIX, *args, file=sys.stderr )


def _error_prefix( critical=False ):
	if critical:
		return "CRITICAL ERROR"
	else:
		return "ERROR"


def print_error( *args, critical=False ):
	"""
	Print error message on console.
	"""

	print( _error_prefix(critical), *args, file=sys.stderr )
