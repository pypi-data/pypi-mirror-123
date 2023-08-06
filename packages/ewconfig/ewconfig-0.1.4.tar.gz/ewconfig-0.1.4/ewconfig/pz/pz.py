
class PolesZeros:

    def __init__(self):
        self.lat = 0.0
        self.lon = 0.0
        self.elev = 0.0
        self.net = None
        self.sta = None
        self.chan = None
        self.loc = None
        self.constant = 0.0
        self.zeros_lines = []
        self.poles_lines = []
        self.keep_comment = ''

    def __str__(self):
        return f'{self.net}.{self.sta}.{self.chan}.{self.loc}'
