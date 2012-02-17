from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer

from collections import deque

class iViewXception(Exception):
    def __init__(self, cmd, error):
        self.cmd = cmd
        self.error = error
    def __str__(self):
        return repr(self.cmd, self.error)

class iViewX(DatagramProtocol):
    
    deferreds = deque()

    def startProtocol(self):
        host = '128.113.89.129'
        port = 4444

        self.transport.connect(host, port)
        self.test()

    def datagramReceived(self, data, (host, port)):
        print data
        #uid = uuid.uuid4()
        #print data.split('\n\r\n')[0].split()

    def connectionRefused(self):
        print "No one listening"

    def sendCommand(self, cmd):
        #d = defer.Deferred()
        #d.addCallback(cb)
        #self.deferreds.appendleft(d)
        self.transport.write('%s\n' % cmd)
        #return d
        
    """
    Data output
    """
        
    def setDataFormat(self, frm):
        if not isinstance(frm, str):
            raise iViewXception('ET_FRM', 'Not a string')
        self.transport.write('ET_FRM "%s"\n' % frm)
        
    def startDataStreaming(self, framerate=0):
        if isinstance(framerate, int) and framerate > 0:
            self.transport.write('ET_STR %d\n' % framerate)
        else:
            self.transport.write('ET_STR\n')
            
    def stopDataStreaming(self):
        self.transport.write('ET_EST\n')
                
    def getSampleRate(self):
        self.sendCommand('ET_SRT')

    def test(self):
        #self.setDataFormat('%TS %PX %PY %EZ')
        #self.startDataStreaming()
        #sleep(1)
        #self.stopDataStreaming()
        self.getSampleRate()
        #self.setSizeCalibrationArea(1280,1024)
        #calPnts = 5
        #self.startCalibration(calPnts)
        #for i in range(0,calPnts):
        #    self.acceptCalibrationPoint()   
    
        
if __name__ == '__main__':
    
    iViewX = iViewX()
    reactor.listenUDP(4444, iViewX)
    reactor.run()