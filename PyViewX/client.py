"""
.. module:: client
	:platform: Unix

.. moduleauthor:: Ryan Hope <rmh3093@gmail.com>
"""

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

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer

from collections import deque

from exceptions import PyViewXception

class iViewXClient( DatagramProtocol ):
	"""Handles all communication with the iViewX server."""

	deferreds = {}

	def startProtocol( self ):
		host = '128.113.89.57'
		port = 4444

		self.transport.connect( host, port )
		self.test()

	def connectionRefused( self ):
		print "No one listening"

	def __noop( self ):
		pass

	def datagramReceived( self, data, ( host, port ) ):
		data = data.split()
		if self.deferreds.has_key( data[0] ):
			cb = self.deferreds[data[0]].pop()
			cb.callback( data )
		else:
			print ['UNHANDLED', data]

	def __sendCommand( self, *args, **kwargs ):
		if not self.deferreds.has_key( args[0] ):
			self.deferreds[args[0]] = deque()
		d = defer.Deferred()
		if kwargs['callback']:
			d.addCallback( kwargs['callback'] )
		else:
			d.addCallback( self.__noop )
		self.deferreds[args[0]].appendleft( d )
		self.transport.write( '%s\n' % ' '.join( map( str, args ) ) )

	#===========================================================================
	# Calibration
	#===========================================================================

	def startCalibration( self, points, eye = 0, callback = None ):
		"""Start calibration procedure.

		:param points: The number of calibration points; valid options are 2, 5, 9 or 13.
		:type points: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if not ( points == 2 or points == 5 or points == 9 or points == 13 ):
			raise PyViewXception( 'ET_CAL', 'Invalid points' )
		if ( not isinstance( eye, int ) or eye < 0 or eye > 2 ):
			raise PyViewXception( 'ET_CAL', 'Invalid eye' )
		if ( eye == 1 or eye == 2 ):
			self.__sendCommand( 'ET_CAL', points, eye, callback = callback )
		else:
			self.__sendCommand( 'ET_CAL', points, callback = callback )

	def acceptCalibrationPoint( self, callback = None ):
		"""Accept calibration point.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self.__sendCommand( 'ET_ACC', callback = callback )

	def cancelCalibration( self, callback = None ):
		"""Cancel calibration procedure.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self.__sendCommand( 'ET_BRK', callback = callback )

	def getCalibrationParam( self, param, callback = None ):
		"""Get calibration parameter.

		:param param: Numeric ID of calibration parameter; valid options are 0, 1, 2 and 3.
		:type param: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if ( param < 0 or param > 3 ):
			raise PyViewXception( 'ET_CPA', 'Invalid param' )
		self.__sendCommand( 'ET_CPA', param, callback = callback )

	def setCalibrationParam( self, param, value, callback = None ):
		"""Set calibration parameter.

		:param param: Numeric ID of calibration parameter; valid options are 0, 1, 2 and 3.
		:type param: int.
		:param value: New state of calibration parameter; valid options are True=On, False=Off.
		:type value: bool.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if ( param < 0 or param > 3 ):
			raise PyViewXception( 'ET_CPA', 'Invalid param' )
		if not isinstance( value, bool ):
			raise PyViewXception( 'ET_CPA', 'Value not boolean' )
		self.__sendCommand( 'ET_CPA', param, int( value ), callback = callback )

	def setSizeCalibrationArea( self, width, height, callback = None ):
		"""Set the size of the calibration area.

		:param width: Width of calibration area in pixels.
		:type width: int.
		:param height: Height of calibration area in pixels.
		:type height: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if not ( isinstance( width, int ) and isinstance( height, int ) and width > 0 and height > 0 ):
			raise PyViewXception( 'ET_CSZ', 'Invalid dimension' )
		self.__sendCommand( 'ET_CSZ', width, height, callback = callback )

	def resetCalibrationPoints( self, callback = None ):
		"""Reset calibration points to default values.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self.__sendCommand( 'ET_DEF', callback = callback )

	def setCalibrationCheckLevel( self, value, callback = None ):
		"""Set calibration check level.

		:param value: Calibration check level; valid values are 0, 1, 2 or 3.
		:type value: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if ( value < 0 or value > 3 ):
			raise PyViewXception( 'ET_LEV', 'Invalid value' )
		self.__sendCommand( 'ET_LEV', value, callback = callback )

	def setCalibrationPoint( self, point, x, y, callback = None ):
		"""Set location of calibration point.

		:param point: Calibration point.
		:type point: int.
		:param x: Horizontal position of calibration point in pixels.
		:type x: int.
		:param y: Vertical position of calibration point in pixels.
		:type y: int.
		:param callback: A function to call with response.
		:type callback: function.

		.. note::
			Not available on RED systems.

		"""
		if not ( isinstance( point, int ) and point > 0 and point < 14 and isinstance( x, int ) and isinstance( y, int ) and x > 0 and y > 0 ):
			raise PyViewXception( 'ET_PNT', 'Invalid point' )
		self.__sendCommand( 'ET_PNT', point, x, y, callback = callback )

	def startDriftCorrection( self, callback = None ):
		"""Start drift correction.

		:param callback: A function to call with response.
		:type callback: function.

		.. note::
			Only for hi-speed systems.

		"""
		self.__sendCommand( 'ET_DEF', callback = callback )

	def validateCalibrationAccuracy( self, callback = None ):
		"""Validate calibration accuracy.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self.__sendCommand( 'ET_VLS', callback = callback )

	def validateCalibrationAccuracyExtended( self, x, y, callback = None ):
		"""Validate calibration accuracy (extended).

		:param x: Horizontal position of calibration test point in pixels.
		:type x: int.
		:param y: Vertical position of calibration test point in pixels.
		:type y: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if not ( isinstance( x, int ) and isinstance( y, int ) and x > 0 and y > 0 ):
			raise PyViewXception( 'ET_VLX', 'Invalid point' )
		self.__sendCommand( 'ET_VLX', x, y, callback = callback )

	def requestCalibrationResults( self, callback = None ):
		"""Request calibration resuts.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self.__sendCommand( 'ET_RES', callback = callback )

	#===========================================================================
	# Data output
	#===========================================================================

	def setDataFormat( self, frm, callback = None ):
		"""Set the format of streaming data.

		:param frm: The format of the streamed data.
		:type frm: str.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if not isinstance( frm, str ):
			raise PyViewXception( 'ET_FRM', 'Not a string' )
		self.__sendCommand( 'ET_FRM', '"%s"' % frm, callback = callback )

	def startDataStreaming( self, framerate = 0, callback = None ):
		"""Start data streaming.

		:param framerate: Set framerate -- 1..SampleRate. [*optional*]
		:type framerate: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		self.__sendCommand( 'ET_EST', callback = callback )
		if isinstance( framerate, int ) and framerate > 0:
			self.__sendCommand( 'ET_STR', framerate = framerate, callback = callback )
		else:
			self.__sendCommand( 'ET_STR', callback = callback )

	def stopDataStreaming( self, callback = None ):
		"""Stop data streaming.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self.__sendCommand( 'ET_EST', callback = callback )

	#===========================================================================
	# Other
	#===========================================================================

	def getSampleRate( self, callback = None ):
		"""Get sample rate.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self.__sendCommand( 'ET_SRT', callback = callback )
