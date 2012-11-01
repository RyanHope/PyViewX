Here's a basic example of usage::

	from pyviewx.client import iViewXClient
	from pyviewx.pygame import Calibrator
	from twisted.internet import reactor

	client = iViewXClient('192.168.1.100', 4444)
	calibrator = Calibrator(client, reactor = reactor)
	reactor.listenUDP(5555, client)
	reactor.callLater(0, calibrator.start)
	reactor.run()
