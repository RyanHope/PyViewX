# -*- coding:	utf-8 -*-
#===============================================================================
# This file is part of PyViewX.
# Copyright (C) 2012 Ryan Hope <rmh3093@gmail.com>
#
# PyViewX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyViewX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyViewX.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

class iViewXception( Exception ):
	def __init__( self, cmd, error ):
		self.cmd = cmd
		self.error = error
	def __str__( self ):
		return repr( self.cmd, self.error )
