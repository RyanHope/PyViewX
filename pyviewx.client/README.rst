Here's a basic example of usage::

	from pyviewx.client import iViewXClient, Dispatcher
	from twisted.internet import reactor

	d = Dispatcher()
	client = iViewXClient('192.168.1.100', 4444)
	client.addDispatcher(d)

	@d.listen('ET_FIX')
	def PyViewXEvent(inResponse):
		print 'Fixation Start', inResponse

	@d.listen('ET_EFX')
	def PyViewXEvent(inResponse):
		print 'Fixation End', inResponse

	@d.listen('ET_SPL')
	def PyViewXEvent(inResponse):
		print 'Sample', inResponse

	reactor.listenUDP(5555, client)
	reactor.callLater(0, client.setDataFormat, '%TS %ET %SX %SY %DX %DY %EX %EY %EZ')
	reactor.callLater(0, client.startDataStreaming)
	reactor.callLater(0, client.startFixationProcessing)
	reactor.run()