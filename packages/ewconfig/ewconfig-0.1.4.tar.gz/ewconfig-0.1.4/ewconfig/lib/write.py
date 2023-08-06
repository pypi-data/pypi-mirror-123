from logging import getLogger
from os.path import join

from ewconfig.lib.file import assert_empty_dir

log = getLogger(__name__)

INST = 'INST_WILDCARD'
MOD = 'MOD_WILDCARD'
INDEX_SIZE = 10000
TANKSIZE_VAR = '${WSV_TANK_MEGS}'
TANKDIR_VAR = '${WSV_TANK_DIR}'
EWDATA_VAR = '${EW_DATA_DIR}'

NM_IN_M = 1e9


def write_pz_ew(dir, sncl, drop_comment=False, m_to_nm=1):
    with open(join(dir, "%s.%s.%s.%s.sac" % (sncl.net, sncl.sta, sncl.chan, sncl.loc)), "w") as f:
        if not drop_comment:
            f.write(sncl.keep_comment)
        f.write("ZEROS   %d\n" % len(sncl.zeros_lines))
        for line in sncl.zeros_lines:
            f.write(line)
        f.write("POLES   %d\n" % len(sncl.poles_lines))
        for line in sncl.poles_lines:
            f.write(line)
        sncl.constant = sncl.constant / m_to_nm
        if m_to_nm == 1:
            comment = 'UNITS IN M'
        elif m_to_nm == NM_IN_M:
            comment = 'UNITS IN NM'
        else:
            comment = f'UNITS UNKNOWN (FACTOR {m_to_nm:g})'
        f.write(f"* {comment}\nCONSTANT        {sncl.constant:e}\n")


def write_wsv(dir, sacPZs):
    with open(join(dir, 'wsv_chan_list.d'), 'w') as f:
        f.write(
            "#          names       size  (TYPE_TRACEBUF2 only)         (megabytes) (max breaks)     (full path)      Tank\n")
        for s in sacPZs:
            f.write("Tank %s %s %s %s 4096 %s %s %s %d %s/%s/%s.%s.%s.%s.wsv_tnk\n" % \
                    (s.sta, s.chan, s.net, s.loc, INST, MOD, TANKSIZE_VAR, INDEX_SIZE, EWDATA_VAR, TANKDIR_VAR, \
                     s.sta, s.chan, s.net, s.loc))


def write_pick_sta(dir, sacPZs, geophone=False):
    # example from Raton
    #    1     1  T25A  BHZ TA -- 3  40  3 162  500  3  .939  3.  .4  .015 5.  .9961  1200. 132.7   .8  1.5 135000. 8388608
    #    1     1  T25A  BHE TA -- 3  40  3 162  500  3  .939  3.  .4  .015 5.  .9961  1200. 132.7   .8  1.5 135000. 8388608
    #    1     1  T25A  BHN TA -- 3  40  3 162  500  3  .939  3.  .4  .015 5.  .9961  1200. 132.7   .8  1.5 135000. 8388608
    with open(join(dir, 'pick_sta.d'), 'w') as f:
        f.write(
            '#\n #                              MinBigZC       RawDataFilt    LtaFilt         DeadSta          PreEvent\n')
        f.write('# Pick  Pin    Station/   MinSmallZC   MaxMint           StaFilt       RmavFilt           AltCoda\n')
        f.write(
            '# Flag  Numb   Comp/Net   Itr1   MinPeakSize  i9  CharFuncFilt  EventThresh          CodaTerm         Erefs\n')
        f.write(
            '# ----  ----   --------   ----------------------------------------------------------------------------------\n')
        for s in sacPZs:
            if geophone or s.chan.startswith('E'):
                f.write("1 1 %s %s %s %s 3 40 3 300 500 0 .985 0. .0198 .002 3. .9961 1200. 100.0 .8 1.5 50000. 8388608\n" % \
                        (s.sta, s.chan, s.net, s.loc))
            else:
                f.write(
                    "1  1 %s %s %s %s 3  40  3 162  500  3  .939  3.  .4  .015 5.  .9961  1200. 132.7   .8  1.5 135000. 8388608\n" % \
                    (s.sta, s.chan, s.net, s.loc))


def write_hinv_sta(dir, sac_pzs):
    # P02   XR  EHZ  37 05.0890 104 51.1720 17830.0     0.02  0.00  0.00  0.00    0.0000
    with open(join(dir, 'hinv_sta.d'), 'w') as f:
        for s in sac_pzs:
            lat_deg = int(s.lat)
            lat_min = (s.lat - lat_deg) * 60.
            lon_deg = int(s.lon)
            lon_min = (s.lon - lon_deg) * 60.
            if lon_deg > 0:
                lon_char = "E"
            else:
                lon_char = "W"
            if lon_char == "W":
                # remove negative values
                lon_deg = lon_deg * -1.0
                lon_min = lon_min * -1.0
            f.write("%-5s %2s  %3s  %2d %7.4f %3d %7.4f %4d0.0     0.00  0.00  0.00  0.00    0.00%2s\n" % \
                    (s.sta, s.net, s.chan, lat_deg, lat_min, lon_deg, lon_min, int(s.elev), s.loc))


def write_seed_link_stas(dir, ns_dict):
    with open(join(dir, 'slink_imports.d'), 'w') as f:
        for ns in sorted(ns_dict.keys()):
            f.write("Stream   %s_%s \"%s?.D\"\n" % (ns_dict[ns].net, ns_dict[ns].sta, ns_dict[ns].chan[0:2]))


def write_pick_fp(dir, sac_pzs):
    #                                      threshold1
    # Pick  Pin     Sta/Comp           longTermWindow  tUpEvent
    # Flag  Numb    Net/Loc       filterWindow  threshold2
    # ----  ----    --------      -----------------------------
    #    1    00  AVG 2.4 6.0 10.0 8.0 0.2
    #
    # ----  ----   --------   ----------------------------------------------------------------------------------
    # 1  1 ACSO BH1 US 00  2.4 6.0 10.0 8.0 0.2
    with open(join(dir, 'pick_FP_sta.d'), 'w') as f:
        f.write('#                                      threshold1\n')
        f.write('# Pick  Pin     Sta/Comp           longTermWindow  tUpEvent\n')
        f.write('# Flag  Numb    Net/Loc       filterWindow  threshold2\n')
        f.write('# ----  ----    --------      -----------------------------\n')
        for s in sac_pzs:
            f.write("1    1 %s %s %s %s 2.4 6.0 10.0 8.0 0.2\n" % \
                    (s.sta, s.chan, s.net, s.loc))


def write_trig_sta(dir, sac_pzs):
    with open(join(dir, 'trigsta.scnl'), 'w') as f:
        for s in sac_pzs:
            f.write("TrigStation %s %s %s %s\n" % (s.sta, s.chan, s.net, s.loc))


def log_pz(nscl):
    log.info("%s lat=%f lon=%f elev=%f const=%e np=%d nz=%d" %
             (nscl, nscl.lat, nscl.lon,
              nscl.elev, nscl.constant, len(nscl.poles_lines), len(nscl.zeros_lines)))


def write_all(dir, nscls, drop_comment=False, m_to_nm=1, geophone=False):
    # we sort so that the output is constant even if different sources generate nscls in different orders
    nscls = sorted(nscls, key=str)
    chan = assert_empty_dir(join(dir, 'chan'))
    write_wsv(chan, nscls)
    write_pick_sta(chan, nscls, geophone=geophone)
    write_pick_fp(chan, nscls)
    write_hinv_sta(chan, nscls)
    write_trig_sta(chan, nscls)
    eqk_response = assert_empty_dir(join(dir, 'eqk', 'response'))
    ns_dict = {}
    for nscl in nscls:
        write_pz_ew(eqk_response, nscl, drop_comment=drop_comment, m_to_nm=m_to_nm)
        ns = nscl.net + nscl.sta
        if ns not in ns_dict:
            ns_dict[ns] = nscl
    write_seed_link_stas(chan, ns_dict)


def add_write_args(parser, with_drop_comment=True):
    if with_drop_comment:
        parser.add_argument('-d', '--drop-comment', action="store_true",
                            help='Delete the comments from the sac output.')
    else:
        parser.set_defaults(drop_comment=False)
    parser.add_argument('-n', '--nano', action='store_const',
                        const=NM_IN_M, default=1,
                        help='Convert Constant meters into nanometers. '
                             'You must use this option if you are using the default Localmag or GMEW settings. '
                             'If you have enabled the ResponseInMeters option in localmag.d and/or gmew.d, '
                             'then you don\'t need this option.')
    parser.add_argument('-g', '--geophone', action="store_true",
                        help='Treat ALL instruments as Geophones in pick_ew output. '
                             'Otherwise broadband settings are used unless channel starts with E.')
