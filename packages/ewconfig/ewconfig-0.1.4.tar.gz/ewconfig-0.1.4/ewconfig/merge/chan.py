from logging import getLogger
from os import listdir
from os.path import join, exists
from re import compile

from .parser import BaseParser
from .prefer import Prefer
from .slink import SlinkParser

log = getLogger(__name__)

PARSERS = {}


def merge_filtered_chan(old, new, merged, prefer, sort):
    # by the time we get here we've used the filters to select NSCLs from the two directories
    all_files = set(_ls_chan(old)).union(_ls_chan(new))
    for file in sorted(all_files):
        if file in PARSERS:
            Parser = PARSERS[file]
            log.debug(f'Parsing {file} with {Parser}')
            new_parser = Parser(file, prefer, sort)
            new_parser.read(new)
            old_parser = Parser(file, prefer, sort)
            old_parser.read(old)
            old_parser.add(new_parser)
            old_parser.write(merged)
        else:
            log.error(f'No support for {file}')


def _ls_chan(dir):
    chan = join(dir, 'chan')
    if exists(chan):
        return listdir(chan)
    else:
        return []


class RegexParser(BaseParser):
    '''
    Files with an optional header where each line contains NSCL related data.
    Each line is matched against a pattern and compared with the pre-selected NSCLs.
    '''

    def __init__(self, line_regex, file, prefer, sort, header_regex=None):
        self.__line_regex = line_regex
        self.__prefer = prefer
        self.__sort = sort
        self.__header_regex = header_regex
        self.__header = []
        self.__lines = {}
        super().__init__(file)

    def _match_to_key(self, match):
        raise NotImplementedError('_match_to_key')

    def _read(self, file):
        header = True
        for line in file:
            if header:
                if self.__header_regex and self.__header_regex.match(line):
                    self.__header.append(line)
                else:
                    header = False
            if not header:
                match = self.__line_regex.match(line)
                if match:
                    key = self._match_to_key(match)
                    self.__lines[key] = line
                else:
                    raise Exception(f'Could not parse {line} in {self._file}')

    def add(self, new):
        if self.__header != new.__header:
            log.warning(f'Headers differ for {self._file}')
        for key, line in new.__lines.items():
            if key in self.__lines:
                if line != self.__lines[key]:
                    if self.__prefer == Prefer.OLD:
                        log.warning(f'Taking {key} from {self._file} (old)')
                        pass  # already have the old line
                    elif self.__prefer == Prefer.NEW:
                        log.warning(f'Taking {key} from {new._file} (new)')
                        self.__lines[key] = line
                    else:
                        raise Exception(f'Entries differ for {key} in {self._file}')
                else:
                    log.debug(f'Entries consistent for {key} in {self._file}')
            else:
                self.__lines[key] = line

    def _write(self, file):
        for line in self.__header:
            file.write(line)
        sort = sorted if self.__sort else list
        for key in sort(self.__lines.keys()):
            file.write(self.__lines[key])


class NSCL(RegexParser):
    '''
    Selection uses net, sta, chan and loc.
    '''

    def _match_to_key(self, match):
        return f'{match.group("net")}.{match.group("sta")}.{match.group("chan")}.{match.group("loc")}'


class NSC(RegexParser):
    '''
    Selection uses net, sta and chan.
    '''

    def _match_to_key(self, match):
        return f'{match.group("net")}.{match.group("sta")}.{match.group("chan")}'


class NS(RegexParser):
    '''
    Selection uses net and sta.
    '''

    def _match_to_key(self, match):
        return f'{match.group("net")}.{match.group("sta")}'


hash_header = compile(r'^\s*#')
SNC_prefix = compile(r'^\s*(?P<sta>[A-Z0-9]+)\s+(?P<net>[A-Z0-9]+)\s+(?P<chan>[A-Z0-9]+)\s+')
SCN_from_3 = compile(r'\s*\d+\s+\d+\s+(?P<sta>[A-Z0-9]+)\s+(?P<chan>[A-Z0-9]+)\s+(?P<net>[A-Z0-9]+)\s+')
NS_after_Stream =  compile(r'\s*Stream\s*(?P<net>[A-Z0-9]+)_(?P<sta>[A-Z0-9]+)\s+')
SCNL_after_TrigStation = compile(r'\s*TrigStation\s+(?P<sta>[A-Z0-9]+)\s+(?P<chan>[A-Z0-9]+)\s+(?P<net>[A-Z0-9]+)\s+(?P<loc>(?:[A-Z0-9]+|--))')
SCNL_after_Tank = compile(r'\s*Tank\s+(?P<sta>[A-Z0-9]+)\s+(?P<chan>[A-Z0-9]+)\s+(?P<net>[A-Z0-9]+)\s+(?P<loc>(?:[A-Z0-9]+|--))')


class HinvSta(NSC):

    def __init__(self, file, prefer, sort):
        super().__init__(SNC_prefix, file, prefer, sort)


class PickSta(NSC):

    def __init__(self, file, prefer, sort):
        super().__init__(SCN_from_3, file, prefer, sort, hash_header)


class SlinkImports(NS):
    '''
    Old code, no longer used.  File contents are themselves patterns and must be applied to the NSCLS.
    See new code in slink.py
    '''

    def __init__(self, file, prefer, sort):
        super().__init__(NS_after_Stream, file, prefer, sort)


class TrigSta(NSCL):

    def __init__(self, file, prefer, sort):
        super().__init__(SCNL_after_TrigStation, file, prefer, sort)


class WsvChanList(NSCL):

    def __init__(self, file, prefer, sort):
        super().__init__(SCNL_after_Tank, file, prefer, sort, hash_header)


PARSERS['hinv_sta.d'] = HinvSta
PARSERS['pick_FP_sta.d'] = PickSta
PARSERS['pick_sta.d'] = PickSta
PARSERS['slink_imports.d'] = SlinkParser
PARSERS['trigsta.scnl'] = TrigSta
PARSERS['wsv_chan_list.d'] = WsvChanList
