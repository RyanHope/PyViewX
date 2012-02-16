from exception import iViewXception

class CalibrationCommands(object):
    
    def startCalibration(self, points, eye=1):
        if not (points == 2 or points == 5 or points == 9 or points == 13):
            raise iViewXception('ET_CAL', 'Invalid points')
        if not (eye == 1 or eye == 2):
            raise iViewXception('ET_CAL', 'Invalid eye')
        if self.binocular:
            self.transport.write('ET_CAL %d %d\n' % (points, eye))
        else:
            self.transport.write('ET_CAL %d\n' % points)
            
    def acceptCalibrationPoint(self):
        self.transport.write('ET_ACC\n')
        
    def cancelCalibration(self):
        self.transport.write('ET_BRK\n')
        
    def getCalibrationParam(self, param):
        if (param < 0 or param > 3):
            raise iViewXception('ET_CPA', 'Invalid param')
        self.transport.write('ET_CPA %d\n' % param)
    
    def setCalibrationParam(self, param, value):
        if (param < 0 or param > 3):
            raise iViewXception('ET_CPA', 'Invalid param')
        if not isinstance(value, bool):
            raise iViewXception('ET_CPA', 'Value not boolean')
        self.transport.write('ET_CPA %d %d\n' % (param, int(value)))
        
    def setSizeCalibrationArea(self, width, height):
        if not (isinstance(width, int) and isinstance(height, int) and width > 0 and height >0):
            raise iViewXception('ET_CSZ', 'Invalid dimension')
        self.transport.write('ET_CSZ %d %d\n' % (width, height))
        
    def resetCalibrationPoints(self):
        self.transport.write('ET_DEF\n')
    
    def setCalibrationCheckLevel(self, value):
        if (value < 0 or value > 3):
            raise iViewXception('ET_LEV', 'Invalid value')
        self.transport.write('ET_LEV %d\n' % value)
        
    def setCalibrationPoint(self, point, x, y): # NOTE: Not available on RED systems
        if not (isinstance(point, int) and point > 0 and point < 14 and isinstance(x, int) and isinstance(y, int) and x > 0 and y >0):
            raise iViewXception('ET_PNT', 'Invalid point')
        self.transport.write('ET_PNT %d %d %d\n' % (point, x, y))
        
    def startDriftCorrection(self): # NOTE: Only for hi-speed systms
        self.transport.write('ET_DEF\n')
        
    def validateCalibrationAccuracy(self):
        self.transport.write('ET_VLS\n')
        
    def validateCalibrationAccuracyExtended(self, x, y):
        if not (isinstance(x, int) and isinstance(y, int) and x > 0 and y >0):
            raise iViewXception('ET_VLX', 'Invalid point')
        self.transport.write('ET_VLX %d %d\n' % (x, y))
        
    def requestCalibrationResults(self):
        self.transport.write('ET_RES\n')