from exception import iViewXception

class OtherCommands(object):
    
    def setDataFormat(self, frm):
        if not isinstance(frm, str):
            raise iViewXception('ET_FRM', 'Not a string')
        self.transport.write('ET_FRM "%s"\n' % frm) 