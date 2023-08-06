from shutil import rmtree
from unittest import TestCase

from ewconfig.lib.filter import Filter
from ..lib.x2ew import MainMixin
from ..lib.log import LogMixin


class TestR50A(MainMixin, LogMixin, TestCase):

    stderr_verbosity = 5

    def test_original(self):
        dest_dir = self.run_sac2ew('R50A')
        # fails because we have no way of restricting date range
        with self.assertRaises(AssertionError):
            self.assert_files(dest_dir, 'R50A', rdseed=True)
        rmtree(dest_dir)

    def test_station_xml(self):
        # note that we need to supply default date (not supplied by ArgsParser)
        dest_dir = self.run_xml2ew('R50A', chan_filter=Filter('Channel', excludes=['LOG']), lo_precision=True)
        self.assert_files(dest_dir, 'R50A')
        rmtree(dest_dir)
