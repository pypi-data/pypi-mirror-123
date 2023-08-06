from logging import getLogger
from shutil import rmtree
from unittest import TestCase

from ewconfig.merge.prefer import Prefer
from ..lib.log import LogMixin
from ..lib.merge import MainMixin

log = getLogger(__name__)


class TestIssue6(MainMixin, LogMixin, TestCase):

    stderr_verbosity = 5

    def test_merge(self):
        merged = self.run_merge('issue-6-a', ['issue-6-b'], sort=False)
        self.assert_files(merged, 'issue-6-a')
        rmtree(merged)

    def test_conflict_error(self):
        with self.assertRaisesRegex(Exception, 'Entries differ'):
            merged = self.run_merge('issue-6-a', ['issue-6-c'])

    def test_conflict_a(self):
        merged = self.run_merge('issue-6-a', ['issue-6-c'], prefer=Prefer.OLD, sort=False)
        self.assert_files(merged, 'issue-6-a')
        rmtree(merged)

    def test_conflict_abc(self):
        merged = self.run_merge('issue-6-a', ['issue-6-b', 'issue-6-c'], prefer=Prefer.OLD, sort=False)
        self.assert_files(merged, 'issue-6-a')
        rmtree(merged)

    def test_conflict_c(self):
        merged = self.run_merge('issue-6-a', ['issue-6-c'], prefer=Prefer.NEW, sort=False)
        self.assert_files(merged, 'issue-6-c')
        rmtree(merged)
