#!/usr/bin/env python

#===============================================================================
# Copyright (C) 2012 Ryan Hope <rmh3093@gmail.com>
#
# iViewX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iViewX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with iViewX.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer

from collections import deque

import time

class iViewXception( Exception ):
    def __init__( self, cmd, error ):
        self.cmd = cmd
        self.error = error
    def __str__( self ):
        return repr( self.cmd, self.error )

class iViewX( DatagramProtocol ):

    deferreds = {}

    def startProtocol( self ):
        host = '128.113.89.57'
        port = 4444

        self.transport.connect( host, port )
        self.test()

    def connectionRefused( self ):
        print "No one listening"

    def noop( self ):
        pass

    def datagramReceived( self, data, ( host, port ) ):
        data = data.split()
        if self.deferreds.has_key( data[0] ):
            cb = self.deferreds[data[0]].pop()
            cb.callback( data )
        else:
            print ['UNHANDLED', data]

    def sendCommand( self, *args, **kwargs ):
        if not self.deferreds.has_key( args[0] ):
            self.deferreds[args[0]] = deque()
        d = defer.Deferred()
        if kwargs['callback']:
            d.addCallback( kwargs['callback'] )
        else:
            d.addCallback( self.noop )
        self.deferreds[args[0]].appendleft( d )
        self.transport.write( '%s\n' % ' '.join( map( str, args ) ) )

    #===========================================================================
    # Calibration
    #===========================================================================

    def startCalibration( self, points, eye = 0, callback = None ):
        if not ( points == 2 or points == 5 or points == 9 or points == 13 ):
            raise iViewXception( 'ET_CAL', 'Invalid points' )
        if ( not isinstance( eye, int ) or eye < 0 or eye > 2 ):
            raise iViewXception( 'ET_CAL', 'Invalid eye' )
        if ( eye == 1 or eye == 2 ):
            self.sendCommand( 'ET_CAL', points, eye, callback = callback )
        else:
            self.sendCommand( 'ET_CAL', points, callback = callback )

    def acceptCalibrationPoint( self, callback = None ):
        self.sendCommand( 'ET_ACC', callback = callback )

    def cancelCalibration( self, callback = None ):
        self.sendCommand( 'ET_BRK', callback = callback )

    def getCalibrationParam( self, param, callback = None ):
        if ( param < 0 or param > 3 ):
            raise iViewXception( 'ET_CPA', 'Invalid param' )
        self.sendCommand( 'ET_CPA', param, callback = callback )

    def setCalibrationParam( self, param, value, callback = None ):
        if ( param < 0 or param > 3 ):
            raise iViewXception( 'ET_CPA', 'Invalid param' )
        if not isinstance( value, bool ):
            raise iViewXception( 'ET_CPA', 'Value not boolean' )
        self.sendCommand( 'ET_CPA', param, int( value ), callback = callback )

    def setSizeCalibrationArea( self, width, height, callback = None ):
        if not ( isinstance( width, int ) and isinstance( height, int ) and width > 0 and height > 0 ):
            raise iViewXception( 'ET_CSZ', 'Invalid dimension' )
        self.sendCommand( 'ET_CSZ', width, height, callback = callback )

    def resetCalibrationPoints( self, callback = None ):
        self.sendCommand( 'ET_DEF', callback = callback )

    def setCalibrationCheckLevel( self, value, callback = None ):
        if ( value < 0 or value > 3 ):
            raise iViewXception( 'ET_LEV', 'Invalid value' )
        self.sendCommand( 'ET_LEV', value, callback = callback )

    def setCalibrationPoint( self, point, x, y, callback = None ): # NOTE: Not available on RED systems
        if not ( isinstance( point, int ) and point > 0 and point < 14 and isinstance( x, int ) and isinstance( y, int ) and x > 0 and y > 0 ):
            raise iViewXception( 'ET_PNT', 'Invalid point' )
        self.sendCommand( 'ET_PNT', point, x, y, callback = callback )

    def startDriftCorrection( self, callback = None ): # NOTE: Only for hi-speed systms
        self.sendCommand( 'ET_DEF', callback = callback )

    def validateCalibrationAccuracy( self, callback = None ):
        self.sendCommand( 'ET_VLS', callback = callback )

    def validateCalibrationAccuracyExtended( self, x, y, callback = None ):
        if not ( isinstance( x, int ) and isinstance( y, int ) and x > 0 and y > 0 ):
            raise iViewXception( 'ET_VLX', 'Invalid point' )
        self.sendCommand( 'ET_VLX', x, y, callback = callback )

    def requestCalibrationResults( self, callback = None ):
        self.sendCommand( 'ET_RES', callback = callback )

    #===========================================================================
    # Data output
    #===========================================================================

    def setDataFormat( self, frm, callback = None ):
        if not isinstance( frm, str ):
            raise iViewXception( 'ET_FRM', 'Not a string' )
        self.sendCommand( 'ET_FRM', '"%s"' % frm, callback = callback )

    def startDataStreaming( self, framerate = 0, callback = None ):
        if isinstance( framerate, int ) and framerate > 0:
            self.sendCommand( 'ET_STR', framerate = framerate, callback = callback )
        else:
            self.sendCommand( 'ET_STR', callback = callback )

    def stopDataStreaming( self, callback = None ):
        self.sendCommand( 'ET_EST', callback = callback )

    #===========================================================================
    # Other
    #===========================================================================

    def getSampleRate( self, callback = None ):
        self.sendCommand( 'ET_SRT', callback = callback )

    #===========================================================================
    # Test
    #===========================================================================

    def test( self ):
        reactor.callLater( 0, self.setDataFormat, '%TS %PX %PY %EZ' )
        reactor.callLater( 0, self.startDataStreaming, framerate = 1 )
        reactor.callLater( 1, self.setDataFormat, '%TS %PX %PY' )
        reactor.callLater( 2, self.setDataFormat, '%TS %PX %PY %EZ' )
        reactor.callLater( 3, self.stopDataStreaming )
        reactor.callLater( 3, self.getSampleRate )


if __name__ == '__main__':

    iViewX = iViewX()
    reactor.listenUDP( 4444, iViewX )
    reactor.run()
