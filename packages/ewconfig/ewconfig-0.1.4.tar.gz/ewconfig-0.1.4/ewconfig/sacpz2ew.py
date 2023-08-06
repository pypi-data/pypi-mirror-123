'''
a scanner program in python 3 to take SAC PZ files from rdseed -pf and convert
them to localmag and hypoinverse station lists. This is presumed that the 
dataless was complete and had lat/long/elevation for the SCNL

Example output from rdseed -pf
* **********************************
* NETWORK   (KNETWK): TA
* STATION    (KSTNM): R53A
* LOCATION   (KHOLE): 
* CHANNEL   (KCMPNM): BHZ
* CREATED           : 2013-02-05T01:21:15
* START             : 2013-01-13T00:00:00
* END               : 1919-06-29T15:38:39
* DESCRIPTION       : Hurricane, WV, USA
* LATITUDE          : 38.330700 
* LONGITUDE         : -81.951300 
* ELEVATION         : 294.0  
* DEPTH             : 0.0  
* DIP               : 0.0  
* AZIMUTH           : 0.0  
* SAMPLE RATE       : 40.0
* INPUT UNIT        : M
* OUTPUT UNIT       : COUNTS
* INSTTYPE          : Guralp CMG3T/Quanterra 330 Linear Phase Composite
* INSTGAIN          : 1.504200e+03 (M/S)
* COMMENT           : T3P01 0100000A1B8D11B0
* SENSITIVITY       : 6.309070e+08 (M/S)
* A0                : 5.714000e+08
* **********************************
ZEROS   3
        +0.000000e+00   +0.000000e+00
        +0.000000e+00   +0.000000e+00
        +0.000000e+00   +0.000000e+00
POLES   5
        -3.701000e-02   +3.701000e-02
        -3.701000e-02   -3.701000e-02
        -1.131000e+03   +0.000000e+00
        -1.005000e+03   +0.000000e+00
        -5.027000e+02   +0.000000e+00
CONSTANT        +3.605003e+17
'''

from argparse import ArgumentParser
from logging import getLogger
from os import listdir
from os.path import join
from re import search

from .lib.args import add_version_args
from .lib.file import assert_dir
from .lib.log import add_log_args, make_log_from_args
from .lib.markdown import add_md_help_argument
from .lib.write import log_pz, write_all, add_write_args
from .pz.sac import SacPolesZeros

log = getLogger(__name__)


def read(dir, pz):
    files = listdir(dir)
    sacpz_list = []
    for file in files:
        log.info("working on %s", file)
        if search('^SAC_PZs_.*', file):
            sac = pz(join(dir, file))
            log_pz(sac)
            sacpz_list.append(sac)
    return sacpz_list


def main(dir, drop_comment=False, m_to_nm=1, geophone=False):
    nscls = read(dir, SacPolesZeros)
    write_all(dir, nscls, drop_comment=drop_comment, m_to_nm=m_to_nm, geophone=geophone)


def main_args():
    try:
        parser = ArgumentParser(prog='ewconfig',
                                description="""A scanner program to 
take SAC PZ files from rdseed -pf and convert them to configurations suitable 
for use with localmag, hypoinverse, pick_ew, pick_FP, slink2ew, carlstatrig and
wave_serverV station lists. It is presumed that the dataless was complete and had 
lat/long/elevation for the SCNL. Output sac files will be in Meters unless the
--nano parameter is set to convert to nanometers. The output files will appear
in the current directory.""")
        parser.add_argument('pzdirectory', type=assert_dir,
                            help='Directory containing the input files -- which are the output of rdseed -pf')
        add_write_args(parser)
        add_version_args(parser)
        add_md_help_argument(parser)
        add_log_args(parser)
        args = parser.parse_args()
        make_log_from_args(parser.prog, args)
        main(args.pzdirectory, args.drop_comment, args.nano, args.geophone)
    except Exception as e:
        log.critical(e)
        exit(1)


if __name__ == '__main__':
    main_args()
