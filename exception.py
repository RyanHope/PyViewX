class iViewXception(Exception):
    def __init__(self, cmd, error):
        self.cmd = cmd
        self.error = error
    def __str__(self):
        return repr(self.cmd, self.error)