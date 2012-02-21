#!/usr/bin/env python

from twisted.internet import reactor
from PyViewX.client import iViewXClient

client = iViewXClient( '128.113.89.57', 4444 )
reactor.listenUDP( 4444, client )

reactor.callLater( 1, client.setDataFormat, '%TS %PX %PY %EZ' )
reactor.callLater( 1, client.startDataStreaming, framerate = 1 )
reactor.callLater( 2, client.setDataFormat, '%TS %PX %PY' )
reactor.callLater( 3, client.setDataFormat, '%TS %PX %PY %EZ' )
reactor.callLater( 4, client.stopDataStreaming )
reactor.callLater( 4, client.getSampleRate )

reactor.run()
