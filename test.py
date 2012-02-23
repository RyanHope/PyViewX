#!/usr/bin/env python

from twisted.internet import reactor
from PyViewX.client import iViewXClient
import pygame
import sys

pygame.init()

client = iViewXClient( '127.0.0.1', 4444 )

calibrationPoints = []
surface = None
count = 0

@client.subscribe( needs = ['ET_SPL'] )
def iViewXEvent( *args, **kwargs ):
        global surface
        global count
        print reactor.seconds(), kwargs['ET_SPL']
        if count == 0:
                surface.fill( ( 51, 51, 153 ) )
                pygame.draw.circle( surface, ( 255, 0, 0 ), (int(float( kwargs['ET_SPL'][1] )), int(float( kwargs['ET_SPL'][3] ))), 5 )
                pygame.display.flip()
        count += 1
        if count > 15:
                count = 0

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
	pygame.draw.circle( surface, ( 255, 255, 0 ), calibrationPoints[point-1], 10 )
	pygame.draw.circle( surface, ( 0, 0, 0 ), calibrationPoints[point-1], 5 )
	pygame.display.flip()
	reactor.callLater( 2, client.acceptCalibrationPoint )

@client.subscribe( needs = ['ET_FIN'] )
def iViewXEvent( *args, **kwargs ):
	#pygame.display.quit()
	reactor.callLater( 0, client.requestCalibrationResults )
	reactor.callLater( 0, client.setDataFormat, '%TS %SX %SY' )
	reactor.callLater( 0, client.startDataStreaming, framerate = 30 )

reactor.listenUDP( 5555, client )

reactor.callLater( 0, client.stopDataStreaming )
reactor.callLater( 0, client.getSampleRate )
reactor.callLater( 0, client.setSizeCalibrationArea, 1280, 1024 )
reactor.callLater( 0, client.startCalibration, 5, 1 )

reactor.callLater( 60, sys.exit )

reactor.run()
