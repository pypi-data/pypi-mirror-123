from shutil import rmtree
from unittest import TestCase

from ewconfig.lib.filter import Filter
from ewconfig.pz.xml import Response
from ..lib.x2ew import MainMixin
from ..lib.log import LogMixin


class TestBadUnits(MainMixin, LogMixin, TestCase):

    stderr_verbosity = 5

    def test_station_xml(self):
        dest_dir = self.run_xml2ew('BAD-UNITS', chan_filter=Filter('Channel', excludes=['LOG']),
                                   lo_precision=True)
        with self.assertRaises(AssertionError):
            self.assert_files(dest_dir, 'BAD-UNITS',
                              skip_files=('CI.PASC.VDO.00.sac', 'CI.PASC.VKO.00.sac'),
                              skip_lines=(r'PASC .*VDO', r'PASC .*VKO'))

    def test_station_xml_with_default(self):
        dest_dir = self.run_xml2ew('BAD-UNITS',
                                   chan_filter=Filter('Channel', excludes=['LOG']), lo_precision=True,
                                   default_response=Response.ACCELERATION)
        self.assert_files(dest_dir, 'BAD-UNITS',
                          skip_files=('CI.PASC.VDO.00.sac', 'CI.PASC.VKO.00.sac'),
                          skip_lines=(r'PASC .*VDO', r'PASC .*VKO'))
        rmtree(dest_dir)
