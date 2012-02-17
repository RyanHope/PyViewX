#!/usr/bin/env python

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer

from collections import deque

import time

class iViewXception(Exception):
    def __init__(self, cmd, error):
        self.cmd = cmd
        self.error = error
    def __str__(self):
        return repr(self.cmd, self.error)

class iViewX(DatagramProtocol):
    
    deferreds = {}

    def startProtocol(self):
        host = '128.113.89.57'
        port = 4444

        self.transport.connect(host, port)
        self.test()

    def datagramReceived(self, data, (host, port)):
        data = data.split()
        if self.deferreds.has_key(data[0]):
            cb = self.deferreds[data[0]].pop()
            cb.callback(data)
        else:
            self.dumpReply(data)

    def connectionRefused(self):
        print "No one listening"
        
    def dumpReply(self, reply):
        print reply

    def sendCommand(self, *args, **kwargs):
        if not self.deferreds.has_key(args[0]):
            self.deferreds[args[0]] = deque()
        d = defer.Deferred()
        if kwargs['callback']:
            d.addCallback(kwargs['callback'])
        else:
            d.addCallback(self.dumpReply)
        self.deferreds[args[0]].appendleft(d)
        self.transport.write('%s\n' % ' '.join(map(str,args)))
        return d
        
    # ~~~~~~~~~~~~~~~~~~~~~~ #
    # Data output
    # ~~~~~~~~~~~~~~~~~~~~~~ #
        
    def setDataFormat(self, frm, callback=None):
        if not isinstance(frm, str):
            raise iViewXception('ET_FRM', 'Not a string')
        self.sendCommand('ET_FRM', '"%s"' % frm, callback=callback)
        
    def startDataStreaming(self, framerate=0, callback=None):
        if isinstance(framerate, int) and framerate > 0:
            self.sendCommand('ET_STR', framerate=framerate, callback=callback)
        else:
            self.sendCommand('ET_STR', callback=callback)
            
    def stopDataStreaming(self, callback=None):
        self.sendCommand('ET_EST', callback=callback)

    def getSampleRate(self, callback=None):
        self.sendCommand('ET_SRT', callback=callback)

    def test(self):
        reactor.callLater(0, self.setDataFormat, '%TS %PX %PY %EZ')
        reactor.callLater(0, self.startDataStreaming, framerate=1)
        reactor.callLater(1, self.setDataFormat, '%TS %PX %PY')
        reactor.callLater(2, self.setDataFormat, '%TS %PX %PY %EZ')
        reactor.callLater(3, self.stopDataStreaming)
        reactor.callLater(3, self.getSampleRate)
    
        
if __name__ == '__main__':
    
    iViewX = iViewX()
    reactor.listenUDP(4444, iViewX)
    reactor.run()