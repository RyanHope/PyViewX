=======
PyViewX
=======

``pyviewx`` is library for communicating with SensoMotoric Instruments (SMI) eye
trackers via iViewX.

Here's a basic example of usage::

	from pyviewx import iViewXClient
	from panglery import Pangler
	from twisted.internet import reactor

	pangler = Pangler()

	@pangler.subscribe( event = 'ET_FIX', needs = ['data'] )
	def PyViewXEvent( p, data ):
		print 'Fixation Start', data

	@pangler.subscribe( event = 'ET_EFX', needs = ['data'] )
	def PyViewXEvent( p, data ):
		print 'Fixation End', data

	@pangler.subscribe( event = 'ET_SPL', needs = ['data'] )
	def PyViewXEvent( p, data ):
		print 'Sample', data

	client = iViewXClient( pangler, '127.0.0.1', 4444 )

	reactor.listenUDP( 5555, client )
	reactor.callLater( 0, client.setDataFormat, '%TS %ET %SX %SY %DX %DY %EX %EY %EZ' )
	reactor.callLater( 0, client.startDataStreaming )
	reactor.callLater( 0, client.startFixationProcessing )
	reactor.run()