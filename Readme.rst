=======
PyViewX
=======

``pyviewx`` is a Python package for communicating with SensoMotoric Instruments (SMI) eye
trackers via iViewX.

Here's a basic example of usage::

	from pyviewx import iViewXClient
	from twisted.internet import reactor

	client = iViewXClient()
	client.setRemoteInfo('127.0.0.1', 4444)

	@client.subscribe( event = 'ET_FIX', needs = ['data'] )
	def PyViewXEvent( p, data ):
		print 'Fixation Start', data

	@client.subscribe( event = 'ET_EFX', needs = ['data'] )
	def PyViewXEvent( p, data ):
		print 'Fixation End', data

	@client.subscribe( event = 'ET_SPL', needs = ['data'] )
	def PyViewXEvent( p, data ):
		print 'Sample', data

	reactor.listenUDP( 5555, client )
	reactor.callLater( 0, client.setDataFormat, '%TS %ET %SX %SY %DX %DY %EX %EY %EZ' )
	reactor.callLater( 0, client.startDataStreaming )
	reactor.callLater( 0, client.startFixationProcessing )
	reactor.run()