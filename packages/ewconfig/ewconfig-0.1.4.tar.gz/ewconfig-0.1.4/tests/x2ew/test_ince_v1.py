from shutil import rmtree
from unittest import TestCase

from ..lib.x2ew import MainMixin
from ..lib.log import LogMixin


class TestInceV1(MainMixin, LogMixin, TestCase):

    stderr_verbosity = 5

    def test_original(self):
        dest_dir = self.run_sac2ew('Ince_v1')
        self.assert_files(dest_dir, 'Ince_v1', rdseed=True)
        rmtree(dest_dir)

    def test_station_xml(self):
        dest_dir = self.run_xml2ew('Ince_v1')
        self.assert_files(dest_dir, 'Ince_v1')
        rmtree(dest_dir)
