from argparse import ArgumentParser
from logging import getLogger
from os import getcwd

from obspy import read_inventory
from obspy.io.stationxml.core import validate_stationxml

from .lib.args import ParagraphHelpFormatter, add_version_args
from .lib.date import parse_date, between
from .lib.file import assert_dir
from .lib.filter import Filter
from .lib.log import add_log_args, make_log_from_args
from .lib.markdown import add_md_help_argument
from .lib.write import write_all, add_write_args
from .pz.xml import XmlPolesZeros, Response, UnsupportedResponseException

'''
The equivalent of sacpz2ew, but takes input from station.xml files. 
'''

log = getLogger(__name__)


def _validate(file):
    ok, errors = validate_stationxml(file)
    if not ok:
        log.info('The following warnings are from XML validation:')
        for error in errors:
            log.warning(error)
        # paul's Ince_v1 file triggers warnings
        log.info('End of XML validation warnings')
        log.info('Will continue despite warnings above')


def _parse(metadata, sta_filter, chan_filter, date=None, lo_precision=False, default_response=None):
    for network in metadata.networks:
        for station in sta_filter(network.stations, key=lambda sta: sta.code):
            for channel in chan_filter(station.channels, key=lambda chan: chan.code):
                nscl = f'{network.code}.{station.code}.{channel.code}.' \
                       f'{channel.location_code if channel.location_code else "--"}'
                if between(channel.start_date, date, channel.end_date):
                    try:
                        log.info(f'Processing {nscl}')
                        yield XmlPolesZeros(network, station, channel,
                                            lo_precision=lo_precision, default_response=default_response)
                    except UnsupportedResponseException as e:
                        log.warning(f'Skipping {nscl}: {e}')
                else:
                    log.warning(f'Skipping {nscl}: date range {channel.start_date} - {channel.end_date}')


def main_multiple(files, dirs=None, drop_comment=False, m_to_nm=1, geophone=False,
                  lo_precision=False, default_response=None,
                  sta_filter=Filter('Station'), chan_filter=Filter('Channel'), date=None):
    if len(files) == 1:
        if len(dirs) == 0:
            dirs = [None]
    if len(dirs) != len(files):
        raise Exception('The number of output directories must match the number of XML files.')
    for file, dir in zip(files, dirs):
        log.info(f'Expanding {file} into {dir}')
        main_single(file, dir=dir, drop_comment=drop_comment, m_to_nm=m_to_nm, geophone=geophone,
                    lo_precision=lo_precision, default_response=default_response,
                    sta_filter=sta_filter, chan_filter=chan_filter, date=date)


def main_single(file, dir=None, drop_comment=False, m_to_nm=1, geophone=False,
                lo_precision=False, default_response=None,
                sta_filter=Filter('Station'), chan_filter=Filter('Channel'), date=None):
    log.debug(f'Calling stationxml2ew single for file={file} dir={dir} drop_comment={drop_comment} '
              f'm_to_nm={m_to_nm} geophone={geophone} lo_precision={lo_precision} '
              f'default_response={default_response}sta_filter={sta_filter} chan_filter={chan_filter} '
              f'date={date}')
    _validate(file)
    dir = assert_dir(dir or getcwd(), 'Output dir (--dir)', create=True)
    metadata = read_inventory(file)
    scnls = list(_parse(metadata, sta_filter, chan_filter, date=date,
                        lo_precision=lo_precision, default_response=default_response))
    write_all(dir, scnls, drop_comment=drop_comment, m_to_nm=m_to_nm, geophone=geophone)
    
    
def add_stationxml2ew_args(parser):
    # separated here so that it can also be used by ewmerge
    parser.add_argument('--include-chan', metavar='PATTERN', nargs='*',
                        help='Pattern to match included channel names (default all).')
    parser.add_argument('--exclude-chan', metavar='PATTERN', nargs='*',
                        help='Pattern to match excluded channel names.')
    parser.add_argument('--include-sta', metavar='PATTERN', nargs='*',
                        help='Pattern to match included station names (default all).')
    parser.add_argument('--exclude-sta', metavar='PATTERN', nargs='*',
                        help='Pattern to match excluded station names.')
    parser.add_argument('--date', type=parse_date, help='Use channels valid on this date (default now).')
    defaults = parser.add_mutually_exclusive_group()
    defaults.add_argument('--displacement', dest='default_response', action='store_const',
                          const=Response.DISPLACEMENT, help='Assume unrecognized responses are displacement.')
    defaults.add_argument('--velocity', dest='default_response', action='store_const',
                          const=Response.VELOCITY, help='Assume unrecognized responses are velocity.')
    defaults.add_argument('--acceleration', dest='default_response', action='store_const',
                          const=Response.ACCELERATION, help='Assume unrecognized responses are acceleration.')
    parser.set_defaults(default_response=None)
    add_write_args(parser, with_drop_comment=False)


def main_args():
    try:
        parser = ArgumentParser(prog='stationxml2ew',
                                formatter_class=ParagraphHelpFormatter,
                                description='''A scanner program to 
convert a station.xml file to configurations suitable for use with localmag, hypoinverse, 
pick_ew, pick_FP, slink2ew, carlstatrig and wave_serverV station lists. It is presumed 
that the input file is complete, with lat/long/elevation for the SCNL.  Output sac files 
will be in meters unless the --nano parameter is set to convert to nanometers. 

Stations and channels can be selected using --include-chan (-sta) and --exclude-chan (-sta).
These take patterns that can match any string (*), any character (?), and any character from 
a sequence ([abc]).  If --include-chan (-sta) is not given it is assumed to be "*".  Channels,
for example, are included if they match --include-chan and do not match --exclude-chan.

Specifying --date selects channels active at that time.  By default this is the current time.

Responses types are recognised via the response units.  Unrecognised units can be given a default
using --displacement|--velocity|--acceleration.  If no default is given they are skipped.  Pressure
sensitive stations (units Pa) are always skipped.    
''')
        parser.add_argument('file', nargs='+', help='Station XML file(s)')
        parser.add_argument('--dir', nargs='*', default=[], metavar='DIR',
                            help='Output directory(s) (default CWD for a single input file)')
        add_stationxml2ew_args(parser)
        add_version_args(parser)
        add_md_help_argument(parser)
        add_log_args(parser)
        args = parser.parse_args()
        make_log_from_args(parser.prog, args)
        main_multiple(args.file, dirs=args.dir,
                      drop_comment=args.drop_comment, m_to_nm=args.nano, geophone=args.geophone,
                      default_response=args.default_response, date=args.date,
                      sta_filter=Filter('Station', includes=args.include_sta, excludes=args.exclude_sta),
                      chan_filter=Filter('Channel', includes=args.include_chan, excludes=args.exclude_chan))
    except Exception as e:
        # log.exception(e)
        log.critical(e)
        exit(1)


if __name__ == '__main__':
    main_args()
