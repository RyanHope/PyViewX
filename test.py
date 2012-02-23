#!/usr/bin/env python

from twisted.internet import reactor
from PyViewX.client import iViewXClient
import pygame

pygame.init()

client = iViewXClient( '128.113.89.129', 4444 )

calibrationPoints = []
surface = None

@client.subscribe( needs = ['ET_SPL'] )
def iViewXEvent( *args, **kwargs ):
	print reactor.seconds(), kwargs['ET_SPL']

@client.subscribe( needs = ['ET_SRT'] )
def iViewXEvent( *args, **kwargs ):
	print reactor.seconds(), int( kwargs['ET_SRT'][0] )

@client.subscribe( needs = ['ET_CAL'] )
def iViewXEvent( *args, **kwargs ):
	global calibrationPoints
	calibrationPoints = [None] * int( kwargs['ET_CAL'][0] )
	print reactor.seconds(), calibrationPoints

@client.subscribe( needs = ['ET_CSZ'] )
def iViewXEvent( *args, **kwargs ):
	global surface
	width = int( kwargs['ET_CSZ'][0] )
	height = int( kwargs['ET_CSZ'][1] )
	print reactor.seconds(), width, height
	surface = pygame.display.set_mode( ( width, height ), 0 )
	surface.fill( ( 51, 51, 153 ) )
	pygame.display.flip()

@client.subscribe( needs = ['ET_PNT'] )
def iViewXEvent( *args, **kwargs ):
	global calibrationPoints
	calibrationPoints[int( kwargs['ET_PNT'][0] ) - 1] = ( int( kwargs['ET_PNT'][1] ), int( kwargs['ET_PNT'][2] ) )
	print reactor.seconds(), calibrationPoints

@client.subscribe( needs = ['ET_CHG'] )
def iViewXEvent( *args, **kwargs ):
	global surface
	global calibrationPoints
	point = int( kwargs['ET_CHG'][0] )
	print reactor.seconds(), point
	surface.fill( ( 51, 51, 153 ) )
	pygame.draw.circle( surface, ( 255, 255, 0 ), calibrationPoints[point], 10 )
	pygame.draw.circle( surface, ( 0, 0, 0 ), calibrationPoints[point], 5 )
	pygame.display.flip()
	reactor.callLater( 2, client.acceptCalibrationPoint )



reactor.listenUDP( 4444, client )

#reactor.callLater( 1, client.setDataFormat, '%TS %PX %PY %EZ' )
reactor.callLater( 1, client.startDataStreaming, framerate = 1 )
#reactor.callLater( 2, client.setDataFormat, '%TS %PX %PY' )
#reactor.callLater( 3, client.setDataFormat, '%TS %PX %PY %EZ' )
reactor.callLater( 4, client.stopDataStreaming )
reactor.callLater( 4, client.getSampleRate )

reactor.callLater( 4, client.setSizeCalibrationArea, 1024, 768 )
reactor.callLater( 6, client.startCalibration, 5, 1 )

reactor.run()
