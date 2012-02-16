from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from calibration import CalibrationCommands
from other import OtherCommands

class iViewX(DatagramProtocol, CalibrationCommands, OtherCommands):
    
    binocular = True

    def startProtocol(self):
        host = '128.113.89.57'
        port = 4444

        self.transport.connect(host, port)
        self.setDataFormat('%TS %PX %PY %EZ')

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data.split('\n\r\n')[0], host, port)

    def connectionRefused(self):
        print "No one listening"   
    
        
if __name__ == '__main__':
    
    iViewX = iViewX()
    reactor.listenUDP(4444, iViewX)
    reactor.run()