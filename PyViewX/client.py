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

"""
.. module:: client
	:platform: Linux, MacOSX

.. moduleauthor:: Ryan Hope <rmh3093@gmail.com>
"""

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import defer

from collections import deque

from exceptions import PyViewXception

from panglery import Pangler

class iViewXClient( DatagramProtocol, Pangler ):
	"""Creates an iViewXClient object which handles all communication with
	the iViewX server

	:param remoteHost: The hostname of the iViewX server.
	:type remoteHost: str.
	:param remotePort: The port number the iViewX server listens on for incommming commands.
	:type remotePort: int.

	"""
	deferreds = {}

	def __init__( self, remoteHost = None, remotePort = None, *args, **kwargs ):
		self.remoteHost = remoteHost
		self.remotePort = remotePort
		super( iViewXClient, self ).__init__( *args, **kwargs )

	def startProtocol( self ):
		if self.remoteHost and self.remoteHost:
			self.transport.connect( self.remoteHost, self.remotePort )

	def connectionRefused( self ):
		print "No one listening"

	def _noop( self, data ):
		print ['UNHANDLED', data]

	def datagramReceived( self, data, ( host, port ) ):
		data = data.split()
		self.trigger( e = data[0], event = data[0], data = data[1:] )
		self.trigger( **{data[0]: data[1:]} )
		#print data
		"""cb = self._noop
		if self.deferreds.has_key( data[0] ):
			cb = self.deferreds[data[0]].pop().callback
		if hasattr( self, '_%s' % data[0] ):
			data = getattr( self, '_%s' % data[0] )( data[1:] )
		cb( data )"""

	def _sendCommand( self, *args, **kwargs ):
		"""if kwargs.has_key( 'callback' ) and kwargs['callback']:
			if not self.deferreds.has_key( args[0] ):
				self.deferreds[args[0]] = deque()
			d = defer.Deferred()
			d.addCallback( kwargs['callback'] )
			self.deferreds[args[0]].appendleft( d )"""
		self.transport.write( '%s\n' % ' '.join( map( str, args ) ) )


	#===========================================================================
	# Custom decorator
	#===========================================================================

	def event( self, event ):
		def decorator( target ):
			@self.subscribe( e = event, needs = ['event', 'data'] )
			def wrapper( *args, **kwargs ):
				return target( *args, **kwargs )
			return wrapper
		return decorator

	#===========================================================================
	# Response parsers
	#===========================================================================

	def _ET_SRT( self, data ):
		return int( data[0] )

	def _ET_STR( self, data ):
		return int( data[0] )

	#===========================================================================
	# Calibration
	#===========================================================================

	def startCalibration( self, points, eye = 0, callback = None ):
		"""Starts a calibration. Returns calibration information is successful.

		:param points: The number of calibration points; valid options are 2, 5, 9 or 13.
		:type points: int.
		:param eye: The eye to use for binocular systems; valid options are 1-right or 2-left.
		:type eye: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if not ( points == 2 or points == 5 or points == 9 or points == 13 ):
			raise PyViewXception( 'ET_CAL', 'Invalid points' )
		if ( not isinstance( eye, int ) or eye < 0 or eye > 2 ):
			raise PyViewXception( 'ET_CAL', 'Invalid eye' )
		if ( eye == 1 or eye == 2 ):
			self._sendCommand( 'ET_CAL', points, eye, callback = callback )
		else:
			self._sendCommand( 'ET_CAL', points, callback = callback )

	def acceptCalibrationPoint( self ):
		"""Accepts the current calibration point during the calibration process,
		and switches to the next calibration point. Returns the number of the next
		calibration point if successful. Available only during calibration.

		*The command is sent by iViewX every time a calibration point is accepted
		during calibration, either manually by the user or automatically.*

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self._sendCommand( 'ET_ACC' )

	def cancelCalibration( self, callback = None ):
		"""Cancels the calibration procedure.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self._sendCommand( 'ET_BRK', callback = callback )

	def getCalibrationParam( self, param, callback = None ):
		"""Gets calibration parameters.

		.. note::
			See :func:`setCalibrationParam` for parameter values.

		:param param: Numeric ID of calibration parameter.
		:type param: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if ( param < 0 or param > 3 ):
			raise PyViewXception( 'ET_CPA', 'Invalid param' )
		self._sendCommand( 'ET_CPA', param, callback = callback )

	def setCalibrationParam( self, param, value ):
		"""Sets calibration parameters.

		===== ====================== ======= =======
		param description            value=0 value=1
		===== ====================== ======= =======
		0     wait for valid data    off     on
		1     randomize point order  off     on
		2     auto accept            off     on
		3     calibration speed      slow    fast
		===== ====================== ======= =======

		:param param: Numeric ID of calibration parameter.
		:type param: int.
		:param value: New state of calibration parameter.
		:type value: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if ( param < 0 or param > 3 ):
			raise PyViewXception( 'ET_CPA', 'Invalid param' )
		if not isinstance( value, int ):
			raise PyViewXception( 'ET_CPA', 'Value not boolean' )
		self._sendCommand( 'ET_CPA', param, value )

	def setSizeCalibrationArea( self, width, height, callback = None ):
		"""Sets the size of the calibration area.

		*The command is sent by iViewX when the size of the calibration area is changed.*

		:param width: Width of calibration area in pixels.
		:type width: int.
		:param height: Height of calibration area in pixels.
		:type height: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if not ( isinstance( width, int ) and isinstance( height, int ) and width > 0 and height > 0 ):
			raise PyViewXception( 'ET_CSZ', 'Invalid dimension' )
		self._sendCommand( 'ET_CSZ', width, height, callback = callback )

	def resetCalibrationPoints( self, callback = None ):
		"""Sets all calibration points to default positions.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self._sendCommand( 'ET_DEF', callback = callback )

	def setCalibrationCheckLevel( self, value ):
		"""Sets check level for calibration. Returns the new check level is successful.

		:param value: Calibration check level; valid values are 0=none, 1=weak, 2=medium or 3=strong.
		:type value: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if ( value < 0 or value > 3 ):
			raise PyViewXception( 'ET_LEV', 'Invalid value' )
		self._sendCommand( 'ET_LEV', value )

	def setCalibrationPoint( self, point, x, y, callback = None ):
		"""Sets the position of a given calibration point.

		.. note::
			Not available on RED systems.

		:param point: Calibration point.
		:type point: int.
		:param x: Horizontal position of calibration point in pixels.
		:type x: int.
		:param y: Vertical position of calibration point in pixels.
		:type y: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if not ( isinstance( point, int ) and point > 0 and point < 14 and isinstance( x, int ) and isinstance( y, int ) and x > 0 and y > 0 ):
			raise PyViewXception( 'ET_PNT', 'Invalid point' )
		self._sendCommand( 'ET_PNT', point, x, y, callback = callback )

	def startDriftCorrection( self, callback = None ):
		"""Starts drift correction. Drift correction is available after a
		calibration of the system. Drift correction uses the first calibration
		point, which is usually the center point, as calibration point.

		.. note::
			Only for hi-speed systems.

		:param callback: A function to call with response.
		:type callback: function.
		"""
		self._sendCommand( 'ET_RCL', callback = callback )

	def validateCalibrationAccuracy( self, callback = None ):
		"""Performs a validation of the calibration accuracy. This command is
		available only if a successful calibration has been performed previously.
		The result shows the accuracy of the calibration and therefore indicates
		its quality. With the return values you can estimage before starting the
		experiment, how good the measurement will be.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self._sendCommand( 'ET_VLS', callback = callback )

	def validateCalibrationAccuracyExtended( self, x, y, callback = None ):
		"""Performs an extended calibration validation of a single point. This
		command is available only if a successful calibration has been performed
		previously. THe result shows the accuracy of the calibration and therefore
		indicates its quality. With the return values you can estimate before
		starting the experiment, how good the measurement will be.

		:param x: Horizontal position of calibration test point in pixels.
		:type x: int.
		:param y: Vertical position of calibration test point in pixels.
		:type y: int.
		:param callback: A function to call with response.
		:type callback: function.

		"""
		if not ( isinstance( x, int ) and isinstance( y, int ) and x > 0 and y > 0 ):
			raise PyViewXception( 'ET_VLX', 'Invalid point' )
		self._sendCommand( 'ET_VLX', x, y, callback = callback )

	def requestCalibrationResults( self ):
		"""Requests iViewX for calibration results and returns the gaze data
		aquired for a specific calibration point.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self._sendCommand( 'ET_RES' )

	#===========================================================================
	# Data output
	#===========================================================================

	def setDataFormat( self, frm, callback = None ):
		"""Sets data format for data output. The syntax is similar to the 'C'
		string formatting syntax. Each format specifier is marked by a preceding
		percentage (%) symbol.

		================ ===================================================
		Format specifier Description
		================ ===================================================
		TS               timestamp in milliseconds (0 ...2^64/1000 ms)
		TU               timestamp in microseconds (0 ...2^64 μs)
		DX,DY            pupil diameter (0 ...2^32 pixels) x 32
		PX,PY            pupil position (± 2^31 pixels) x 32
		CX,CY            corneal reflex position (± 2^31 pixels) x 32
		SX,SY            gaze position (± 2^31 pixels)
		SC               scene counter
		ET               eye type information (l-left, r-right, b-binocular)
		================ ===================================================

		Example for monocular data:
			**%TS: %SX, %SY**
		Result:
			**28437864110: 400, 202**

		Example for binocular data:
			**%ET %SX %SY**
		Result:
			**b 399 398 200 199**

		:param frm: The format of the streamed data.
		:type frm: str.

		"""
		if not isinstance( frm, str ):
			raise PyViewXception( 'ET_FRM', 'Not a string' )
		self._sendCommand( 'ET_FRM', '"%s"' % frm )

	def startDataStreaming( self, framerate = 0 ):
		"""Starts continuous data output (streaming) using the output format
		specified with the :func:`setDataFormat` command. Optionally, the
		frame rate can be set at which the data will be streamed.

		:param framerate: Set framerate -- 1..SampleRate. [*optional*]
		:type framerate: int.

		"""
		if isinstance( framerate, int ) and framerate > 0:
			self._sendCommand( 'ET_STR', framerate = framerate )
		else:
			self._sendCommand( 'ET_STR' )

	def stopDataStreaming( self ):
		"""Stops continuous data output (streaming).

		"""
		self._sendCommand( 'ET_EFX' )

	#===========================================================================
	# Online Fixation Detection
	#===========================================================================

	def startFixationProcessing( self, duration = 75, dispersion = 45 ):
		self._sendCommand( 'ET_FIX', duration, dispersion )

	def stopFixationProcessing( self ):
		self._sendCommand( 'ET_EFX' )

	#===========================================================================
	# Other
	#===========================================================================

	def autoAdjust( self ):
		self._sendCommand( 'ET_AAD' )

	def getSampleRate( self, callback = None ):
		"""Returns current sample rate.

		:param callback: A function to call with response.
		:type callback: function.

		"""
		self._sendCommand( 'ET_SRT', callback = callback )
