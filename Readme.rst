=======
PyViewX
=======

``pyviewx`` is a Python package for communicating with SensoMotoric Instruments (SMI) eye
trackers via iViewX.

Here's a basic example of usage::

	from pyviewx import iViewXClient, Dispatcher
	from twisted.internet import reactor

	d = Dispatcher()
	client = iViewXClient(d, '127.0.0.1', 4444)

	@d.listen( 'ET_FIX' )
	def PyViewXEvent( inSender, inEvent, inResponse ):
		print 'Fixation Start', inSender, inEvent, inResponse

	@d.listen( 'ET_EFX' )
	def PyViewXEvent( inSender, inEvent, inResponse ):
		print 'Fixation End', inSender, inEvent, inResponse

	@d.listen( 'ET_SPL' )
	def PyViewXEvent( inSender, inEvent, inResponse ):
		print 'Sample', inSender, inEvent, inResponse

	reactor.listenUDP( 5555, client )
	reactor.callLater( 0, client.setDataFormat, '%TS %ET %SX %SY %DX %DY %EX %EY %EZ' )
	reactor.callLater( 0, client.startDataStreaming )
	reactor.callLater( 0, client.startFixationProcessing )
	reactor.run()