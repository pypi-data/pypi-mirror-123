from enum import Enum

from .pz import PolesZeros


class State(Enum):
    NORMAL = 0
    POLES = 1
    ZEROS = 2


class SacPolesZeros(PolesZeros):

    def __init__(self, file):
        super().__init__()
        self.__num_poles = 0
        self.__num_zeros = 0
        self.__parse(file)

    def __parse(self, file):
        with open(file, 'r') as lines:
            state = State.NORMAL
            for line in lines:
                if state == State.POLES:
                    self.poles_lines.append(line)
                    if len(self.poles_lines) == self.__num_poles:
                        state = State.NORMAL
                    continue
                if state == State.ZEROS:
                    # in zero gathering state
                    self.zeros_lines.append(line)
                    if len(self.zeros_lines) == self.__num_zeros:
                        state = State.NORMAL
                    continue
                a = line.strip().split()
                if a[0] == 'CONSTANT':
                    self.constant = float(a[1])
                    continue
                if a[0] == 'POLES':
                    self.__num_poles = int(a[1])
                    state = State.POLES if self.__num_poles else State.NORMAL
                    continue
                if a[0] == 'ZEROS':
                    self.__num_zeros = int(a[1])
                    state = State.ZEROS if self.__num_zeros else State.NORMAL
                    continue
                if a[0] == '*':
                    # a comment, check for lat, lon, elev, SCNL
                    self.keep_comment = self.keep_comment + line;
                    if a[1] == 'NETWORK':
                        self.net = a[3]
                        continue
                    if a[1] == 'STATION':
                        self.sta = a[3]
                        continue
                    if a[1] == 'CHANNEL':
                        self.chan = a[3]
                        continue
                    if a[1] == 'LOCATION':
                        if len(a) == 4:
                            self.loc = a[3]
                        else:
                            self.loc = '--'
                        continue
                    if a[1] == 'LATITUDE':
                        self.lat = float(a[3])
                        continue
                    if a[1] == 'LONGITUDE':
                        self.lon = float(a[3])
                        continue
                    if a[1] == 'ELEVATION':
                        self.elev = float(a[3])
                        continue

