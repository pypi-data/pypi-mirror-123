from os.path import join
from shutil import rmtree
from unittest import TestCase

from ewconfig.lib.filter import Filter
from ewconfig.lib.write import NM_IN_M
from ..lib.x2ew import MainMixin
from ..lib.log import LogMixin


class TestCiPasc(MainMixin, LogMixin, TestCase):

    stderr_verbosity = 5

    def test_original(self):
        dest_dir = self.run_sac2ew('CI-PASC')
        self.assert_files(dest_dir, 'CI-PASC', rdseed=True)
        rmtree(dest_dir)

    def test_station_xml(self):
        dest_dir = self.run_xml2ew('CI-PASC', chan_filter=Filter('Channel', excludes=['LOG']), lo_precision=True)
        # ignore pressure sensitive channels which are now excluded
        self.assert_files(dest_dir, 'CI-PASC',
                          skip_files=('CI.PASC.VDO.00.sac', 'CI.PASC.VKO.00.sac'),
                          skip_lines=(r'PASC .*VDO', r'PASC .*VKO'))
        rmtree(dest_dir)

    def test_station_xml_nm(self):
        dest_dir = self.run_xml2ew('CI-PASC', chan_filter=Filter('Channel', excludes=['LOG']), lo_precision=True,
                                   m_to_nm=NM_IN_M)
        # everything else has already been tested in previous test
        with open(join(dest_dir, 'eqk/response/CI.PASC.BHE.00.sac')) as sac:
            text = sac.read()
            self.assertTrue('* UNITS IN NM\nCONSTANT        2.925447e+04' in text, text)
        rmtree(dest_dir)
