from logging import getLogger

from .parser import BaseParser
from .prefer import Prefer

'''
https://ds.iris.edu/ds/nodes/dmc/manuals/slink2ew/

#
Selectors      "BH?.D"           # SeedLink selectors.  These selectors are used
                                 # for a uni-station mode connection.  If one
                                 # or more 'Stream' entries are given these are
                                 # used as default selectors for multi-station
                                 # mode data streams.  See description of
                                 # SeedLink selectors below.  Multiple selectors
                                 # must be enclosed in quotes.
#
#
# List each data stream (a network and station code pair) that you
# wish to request from the server with a "Stream" command.  If one or
# more Stream commands are given the connection will be configured in
# multi-station mode (multiple station data streams over a single
# network connection).  If no Stream commands are specified the
# connection will be configured in uni-station mode, optionally using
# any specified "Selectors".  A Stream command should be followed by a
# stream key, a network code followed by a station code separated by
# an underscore (i.e. IU_KONO).  SeedLink selectors for a specific
# stream may optionally be specified after the stream key.  Multiple
# selectors must be enclosed in quotes.  Any selectors specified with
# the Selectors command above are used as defaults when no selectors
# are specified for a given stream.
#
# Combined with the above specified default selectors the BHx channels
# will be requested for each of these stations except for DSB for which
# we also want the LHx channels.
#
Stream  GE_DSB   "BH?.D LH?.D"
Stream  GE_ISP
Stream  GE_APE
Stream  GE_STU
#
#
# Some SeedLink servers support extended selection capability allowing
# wildcards (either '*' or '?') in the network and station fields, for example
# to select all stations from the TA network:
#
Stream TA_*
'''

log = getLogger(__name__)


class SlinkParser(BaseParser):
    '''
    To keep life simple:
    * Comments are not propagated if they are on the same line as data that can be merged.
    * Selectors and Streams are moved to the bottom of the file.
    * Tests for conflicts between old and new ignore patterns (treat everything as text)
    '''

    def __init__(self, file, prefer, sort):
        super().__init__(file)
        self.__prefer = prefer
        self.__sort = sort
        self.__other = []
        # not private only to ease testing
        self._selectors = []
        self._streams = {}

    def _read(self, file):
        for line in file:
            if line.strip().startswith('Stream'):
                self.__read_stream(line)
            elif line.strip().startswith('Selectors'):
                self.__read_selectors(line)
            else:
                self.__other.append(line)

    def __read_stream(self, line):
        tokens = self.__parse_tokens(line)
        if len(tokens) < 2:
            raise Exception(f'Cannot parse "{line}" in {self._file}')
        tokens = tokens[1:]
        if tokens:
            if tokens[0] in self._streams:
                raise Exception(f'Duplicate Stream {tokens[0]} in {self._file}')
            self._streams[tokens[0]] = tokens[1:]

    def __read_selectors(self, line):
        # since this is the global default there should presumably only be one line
        # but rather than throw an error on multiple lines we'll simply append to a single list
        tokens = self.__parse_tokens(line)
        if len(tokens) < 2:
            raise Exception(f'Cannot parse "{line}" in {self._file}')
        tokens = tokens[1:]
        if tokens:
            log.debug(f'Default selectors {", ".join(tokens)} from {self._file}')
            self._selectors.extend(tokens)
        else:
            log.warning(f'Lost all default selectors from {self._file}')

    def __parse_tokens(self, line):
        # all we do here is strip quotes, break into words, and quit if there's a comment
        tokens = []
        token = ''
        for char in line:
            if char in (' ', '\t', '\n', '"', "'"):
                if token:
                    tokens.append(token)
                token = ''
            elif char == '#':
                break
            else:
                token += char
        if token:
            tokens.append(token)
        return tokens

    def add(self, new):
        # the only conflicts we resolve (check) are in streams
        prev_selectors = " ".join(self._selectors)
        for selector in new._selectors:
            if selector not in self._selectors:  # avoid sets to keep ordering
                self._selectors.extend(new._selectors)
        next_selectors = " ".join(self._selectors)
        # warn about this because it applies to all streams
        # an alternative would be to move the default to the streams before merge
        if prev_selectors != next_selectors:
            log.warning(f'Default Selectors for {self._file} changed from '
                        f'{prev_selectors} to {next_selectors}')
        for net_sta, selectors in new._streams.items():
            if net_sta in self._streams:
                if self.__prefer == Prefer.OLD:
                    log.warning(f'Taking {net_sta} from {self._file} (old)')
                    pass  # already have the old data
                elif self.__prefer == Prefer.NEW:
                    log.warning(f'Taking {net_sta} from {new._file} (new)')
                    self._streams[net_sta] = selectors
                elif set(selectors) != set(self._streams[net_sta]):
                    raise Exception(f'Inconsistent selectors for Stream {net_sta} in {self._file}')
            else:
                self._streams[net_sta] = selectors

    def _write(self, file):
        for line in self.__other:
            file.write(line)
        if self._selectors:
            file.write(f'Selectors    "{" ".join(self._selectors)}"\n')
        sort = sorted if self.__sort else list
        for net_sta in sort(self._streams.keys()):
            selectors = self._streams[net_sta]
            if selectors:
                file.write(f'Stream   {net_sta} "{" ".join(selectors)}"\n')
            else:
                file.write(f'Stream   {net_sta}\n')
