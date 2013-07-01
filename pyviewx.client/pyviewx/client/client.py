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
from panglery import Pangler

class Dispatcher(Pangler):

	def listen(self, event):
		def decorator(target):
			@self.subscribe(e=event, needs=['inResponse'])
			def wrapper(*args, **kwargs):
				newargs = tuple([arg for arg in args if not isinstance(arg, Pangler)])
				return target(*newargs, **kwargs)
			return wrapper
		return decorator
	
class iViewXception( Exception ):
	def __init__( self, cmd, error ):
		self.cmd = cmd
		self.error = error
	def __str__( self ):
		return repr( self.cmd, self.error )

class iViewXClient(DatagramProtocol):
	"""Creates an iViewXClient object which handles all communication with
	the iViewX server

	:param remoteHost: The hostname of the iViewX server.
	:type remoteHost: str.
	:param remotePort: The port number the iViewX server listens on for incommming commands.
	:type remotePort: int.

	"""

	def __init__(self, remoteHost, remotePort):
		self.remoteHost = remoteHost
		self.remotePort = remotePort
		self.dispatchers = []

	def addDispatcher(self, dispatcher):
		if not dispatcher in self.dispatchers:
			self.dispatchers.append(dispatcher)

	def removeDispatcher(self, dispatcher):
		if dispatcher in self.dispatchers:
			self.dispatchers.remove(dispatcher)

	def connectionRefused(self):
		for d in self.dispatchers:
			d.trigger(e="CONNECTION_REFUSED", inResponse=None)

	def datagramReceived(self, data, (host, port)):
		data = data.split()
		for d in self.dispatchers:
			d.trigger(e=data[0], inResponse=data[1:])

	def _sendCommand(self, *args, **kwargs):
		self.transport.write('%s\n' % ' '.join(map(str, args)), (self.remoteHost, self.remotePort))

	#===========================================================================
	# Calibration
	#===========================================================================

	def startCalibration(self, points, eye=0):
		"""Starts a calibration. Returns calibration information is successful.

		:param points: The number of calibration points; valid options are 2, 5, 9 or 13.
		:type points: int.
		:param eye: The eye to use for binocular systems; valid options are 1-right or 2-left.
		:type eye: int.

		"""
		if not (points == 2 or points == 5 or points == 9 or points == 13):
			raise iViewXception('ET_CAL', 'Invalid points')
		if (not isinstance(eye, int) or eye < 0 or eye > 2):
			raise iViewXception('ET_CAL', 'Invalid eye')
		if (eye == 1 or eye == 2):
			self._sendCommand('ET_CAL', points, eye)
		else:
			self._sendCommand('ET_CAL', points)

	def acceptCalibrationPoint(self):
		"""Accepts the current calibration point during the calibration process,
		and switches to the next calibration point. Returns the number of the next
		calibration point if successful. Available only during calibration.

		*The command is sent by iViewX every time a calibration point is accepted
		during calibration, either manually by the user or automatically.*

		"""
		self._sendCommand('ET_ACC')

	def cancelCalibration(self):
		"""Cancels the calibration procedure.

		"""
		self._sendCommand('ET_BRK')

	def getCalibrationParam(self, param):
		"""Gets calibration parameters.

		.. note::
			See :func:`setCalibrationParam` for parameter values.

		:param param: Numeric ID of calibration parameter.
		:type param: int.

		"""
		if (param < 0 or param > 3):
			raise iViewXception('ET_CPA', 'Invalid param')
		self._sendCommand('ET_CPA', param)

	def setCalibrationParam(self, param, value):
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

		"""
		if (param < 0 or param > 3):
			raise iViewXception('ET_CPA', 'Invalid param')
		if not isinstance(value, int):
			raise iViewXception('ET_CPA', 'Value not boolean')
		self._sendCommand('ET_CPA', param, value)

	def setSizeCalibrationArea(self, width, height):
		"""Sets the size of the calibration area.

		*The command is sent by iViewX when the size of the calibration area is changed.*

		:param width: Width of calibration area in pixels.
		:type width: int.
		:param height: Height of calibration area in pixels.
		:type height: int.

		"""
		if not (isinstance(width, int) and isinstance(height, int) and width > 0 and height > 0):
			raise iViewXception('ET_CSZ', 'Invalid dimension')
		self._sendCommand('ET_CSZ', width, height)

	def resetCalibrationPoints(self):
		"""Sets all calibration points to default positions.

		"""
		self._sendCommand('ET_DEF')

	def setCalibrationCheckLevel(self, value):
		"""Sets check level for calibration. Returns the new check level is successful.

		:param value: Calibration check level; valid values are 0=none, 1=weak, 2=medium or 3=strong.
		:type value: int.

		"""
		if (value < 0 or value > 3):
			raise iViewXception('ET_LEV', 'Invalid value')
		self._sendCommand('ET_LEV', value)

	def setCalibrationPoint(self, point, x, y):
		"""Sets the position of a given calibration point.

		.. note::
			Not available on RED systems.

		:param point: Calibration point.
		:type point: int.
		:param x: Horizontal position of calibration point in pixels.
		:type x: int.
		:param y: Vertical position of calibration point in pixels.
		:type y: int.

		"""
		if not (isinstance(point, int) and point > 0 and point < 14 and isinstance(x, int) and isinstance(y, int) and x > 0 and y > 0):
			raise iViewXception('ET_PNT', 'Invalid point')
		self._sendCommand('ET_PNT', point, x, y)

	def startDriftCorrection(self):
		"""Starts drift correction. Drift correction is available after a
		calibration of the system. Drift correction uses the first calibration
		point, which is usually the center point, as calibration point.

		.. note::
			Only for hi-speed systems.

		"""
		self._sendCommand('ET_RCL')

	def validateCalibrationAccuracy(self):
		"""Performs a validation of the calibration accuracy. This command is
		available only if a successful calibration has been performed previously.
		The result shows the accuracy of the calibration and therefore indicates
		its quality. With the return values you can estimage before starting the
		experiment, how good the measurement will be.


		"""
		self._sendCommand('ET_VLS')

	def validateCalibrationAccuracyExtended(self, x, y):
		"""Performs an extended calibration validation of a single point. This
		command is available only if a successful calibration has been performed
		previously. THe result shows the accuracy of the calibration and therefore
		indicates its quality. With the return values you can estimate before
		starting the experiment, how good the measurement will be.

		:param x: Horizontal position of calibration test point in pixels.
		:type x: int.
		:param y: Vertical position of calibration test point in pixels.
		:type y: int.

		"""
		if not (isinstance(x, int) and isinstance(y, int) and x > 0 and y > 0):
			raise iViewXception('ET_VLX', 'Invalid point')
		self._sendCommand('ET_VLX', x, y)

	def requestCalibrationResults(self):
		"""Requests iViewX for calibration results and returns the gaze data
		aquired for a specific calibration point.

		"""
		self._sendCommand('ET_RES')

	#===========================================================================
	# Data output
	#===========================================================================

	def setDataFormat(self, frm):
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
		if not isinstance(frm, str):
			raise iViewXception('ET_FRM', 'Not a string')
		self._sendCommand('ET_FRM', '"%s"' % frm)

	def startDataStreaming(self, framerate=0):
		"""Starts continuous data output (streaming) using the output format
		specified with the :func:`setDataFormat` command. Optionally, the
		frame rate can be set at which the data will be streamed.

		:param framerate: Set framerate -- 1..SampleRate. [*optional*]
		:type framerate: int.

		"""
		if isinstance(framerate, int) and framerate > 0:
			self._sendCommand('ET_STR', framerate=framerate)
		else:
			self._sendCommand('ET_STR')

	def stopDataStreaming(self):
		"""Stops continuous data output (streaming).

		"""
		self._sendCommand('ET_EST')

	#===========================================================================
	# Eye video image commands
	#===========================================================================

	def startEyeVideoStreaming(self):
		self._sendCommand('ET_SIM')

	def stopEyeVideoStreaming(self):
		self._sendCommand('ET_EIM')

	#===========================================================================
	# Online Fixation Detection
	#===========================================================================

	def startFixationProcessing(self, duration=75, dispersion=45):
		self._sendCommand('ET_FIX', duration, dispersion)

	def stopFixationProcessing(self):
		self._sendCommand('ET_EFX')

	#===========================================================================
	# Other
	#===========================================================================

	def autoAdjust(self):
		self._sendCommand('ET_AAD')

	def getSampleRate(self):
		"""Returns current sample rate.

		"""
		self._sendCommand('ET_SRT')
