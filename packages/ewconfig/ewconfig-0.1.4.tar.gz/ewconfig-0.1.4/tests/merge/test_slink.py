from os.path import join
from unittest import TestCase

from ewconfig.merge.prefer import Prefer
from ewconfig.merge.slink import SlinkParser
from ..lib.file import project_root
from ..lib.log import LogMixin


class TestSlink(LogMixin, TestCase):

    stderr_verbosity = 5

    def test_parse(self):
        slink = SlinkParser('slink_imports.d', Prefer.CHECK, True)
        slink.read(join(project_root(), 'data', 'reference'))
        self.assertEqual(slink._selectors, ['BH?.D'])
        self.assertEqual(slink._streams, {'GE_APE': [],
                                          'GE_DSB': ['BH?.D', 'LH?.D'],
                                          'GE_ISP': [],
                                          'GE_STU': [],
                                          'TA_*': []})

    def test_idempotent(self):
        old = SlinkParser('slink_imports.d', Prefer.CHECK, True)
        old.read(join(project_root(), 'data', 'reference'))
        new = SlinkParser('slink_imports.d', Prefer.CHECK, True)
        new.read(join(project_root(), 'data', 'reference'))
        old.add(new)
        self.assertEqual(new._selectors, old._selectors)
        self.assertEqual(new._streams, old._streams)

    def test_merge_conflict(self):
        old = SlinkParser('slink_imports.d', Prefer.CHECK, True)
        old.read(join(project_root(), 'data', 'reference'))
        new = SlinkParser('slink_imports-conflict.d', Prefer.CHECK, True)
        new.read(join(project_root(), 'data', 'reference'))
        with self.assertRaisesRegex(Exception, 'Inconsistent selectors'):
            old.add(new)

    def test_merge_old(self):
        old = SlinkParser('slink_imports.d', Prefer.OLD, True)
        old.read(join(project_root(), 'data', 'reference'))
        new = SlinkParser('slink_imports-conflict.d', Prefer.OLD, True)
        new.read(join(project_root(), 'data', 'reference'))
        old.add(new)
        old_old = SlinkParser('slink_imports.d', Prefer.OLD, True)
        old_old.read(join(project_root(), 'data', 'reference'))
        self.assertEqual(old_old._selectors, old._selectors)
        self.assertEqual(old_old._streams, old._streams)

    def test_merge_new(self):
        old = SlinkParser('slink_imports.d', Prefer.NEW, True)
        old.read(join(project_root(), 'data', 'reference'))
        new = SlinkParser('slink_imports-conflict.d', Prefer.NEW, True)
        new.read(join(project_root(), 'data', 'reference'))
        old.add(new)
        old_new = SlinkParser('slink_imports-conflict.d', Prefer.NEW, True)
        old_new.read(join(project_root(), 'data', 'reference'))
        self.assertEqual(old_new._selectors, old._selectors)
        self.assertEqual(old_new._streams, old._streams)

