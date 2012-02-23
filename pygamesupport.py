import pygame

def _update( callback, fps, reactor ):
	if not callback():
		reactor.stop()
	else:
		reactor.callLater( 1.0 / fps , _update, callback, fps, reactor )

def install( callback, fps = 30, reactor = None ):

	if reactor is None:
		from twisted.internet import reactor
	if callback:
		_update( callback, fps, reactor, pygame.time.Clock() )

__all__ = ["install"]
