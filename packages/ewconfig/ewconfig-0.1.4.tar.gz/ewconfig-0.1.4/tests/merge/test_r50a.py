from filecmp import dircmp
from logging import getLogger
from re import search
from shutil import rmtree
from unittest import TestCase

from ewconfig.lib.filter import Filter
from ..lib.log import LogMixin, CaptureLog
from ..lib.merge import MainMixin

log = getLogger(__name__)


class TestR50A(MainMixin, LogMixin, TestCase):

    stderr_verbosity = 5

    def test_merge_ci_pasc(self):
        merged = self.run_merge('R50A', ['CI-PASC'])
        self.assert_files(merged, 'R50A', subdir='merge_ci_pasc', extra_dirs=('extra_dir',))
        rmtree(merged)

    def test_merge_ci_pasc_xml(self):
        # tweak various things because station xml and sacp conversion are not perfectly identical
        merged = self.run_merge('R50A', ['CI-PASC.xml'], chan_filter=Filter('Channel', excludes=['LOG']),
                                lo_precision=True)
        # ignore pressure sensitive channels which are now excluded
        self.assert_files(merged, 'R50A', subdir='merge_ci_pasc', extra_dirs=('extra_dir',),
                          skip_files=('CI.PASC.VDO.00.sac', 'CI.PASC.VKO.00.sac'),
                          skip_lines=(r'PASC .*VDO', r'PASC .*VKO'))
        rmtree(merged)

    def test_merge_duplicates(self):
        with CaptureLog() as log:
            merged = self.run_merge('R50A', ['R50A'], lo_precision=True)
        # we should ONLY check the ambiguous channel
        self.assertTrue(search(r'Compared .*/N4\.R50A\.HH1\.00.sac', log.out), log.out)
        self.assertTrue(search(r'Compared .*/N4\.R50A\.HH2\.00.sac', log.out), log.out)
        self.assertTrue(search(r'Compared .*/N4\.R50A\.HHZ\.00.sac', log.out), log.out)
        self.assert_files(merged, 'R50A', subdir='merge_duplicates', extra_dirs=('extra_dir',))
        rmtree(merged)

    def test_merge_ci_pasc_forced(self):
        backup, old, merged = self.run_merge('R50A', ['CI-PASC'], force=True)
        self.assert_files(merged, 'R50A', subdir='merge_ci_pasc', extra_dirs=('extra_dir',))
        rmtree(merged)
        log.info(f'{old} v {backup}')
        cmp = dircmp(old, backup)
        cmp.report_full_closure()
        self.assertFalse(cmp.left_only)
        self.assertFalse(cmp.right_only)
        self.assertFalse(cmp.diff_files)
        self.assertFalse(cmp.funny_files)
        rmtree(backup)

    def test_merge_ci_pasc_forced_no_backup(self):
        backup, old, merged = self.run_merge('R50A', ['CI-PASC'], force=True, backup='NONE')
        self.assert_files(merged, 'R50A', subdir='merge_ci_pasc', extra_dirs=('extra_dir',))
        rmtree(merged)
        self.assertEqual(None, backup)

