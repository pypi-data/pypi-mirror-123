from itertools import zip_longest
from logging import getLogger
from os import listdir, rmdir
from os.path import join, exists
from re import search
from shutil import copytree

from ewconfig.lib.file import tmp_dir
from .compare import Compare
from ..lib.file import project_root

log = getLogger(__name__)


class MainMixin(Compare):

    def _src_dir(self, name):
        # use the conversion test targets as input
        return join(project_root(), 'data', name.lower(), 'x2ew')

    def _src_dir_or_xml(self, name):
        if name.endswith('.xml'):
            return join(project_root(), 'data', name.split('.')[0].lower(), name)
        else:
            return self._src_dir(name)

    def _test_dir(self, name, subdir):
        return join(project_root(), 'data', name.lower(), subdir)

    def run_merge(self, old, news, force=False, **kwargs):
        from ewconfig.ewmerge import main
        old_dir = self._src_dir(old)
        new_dirs = [self._src_dir_or_xml(new) for new in news]
        if force:
            # need to copy old_dir since we don't want to actually overwrite it
            tmp_old_dir = tmp_dir()
            rmdir(tmp_old_dir)
            copytree(old_dir, tmp_old_dir)
            # returns backup, old_dir and tmp_old_dir (merged, which needs to be passed to assert_files)
            # (so old_dir is the original, tmp_old_dir is a copy we made so that overwriting wouldn't
            # erase the test data, and backup is the backed-up copy of tmp_old_dir)
            return main(tmp_old_dir, new_dirs, force=True, **kwargs), old_dir, tmp_old_dir
        else:
            # returns merged
            return main(old_dir, new_dirs, force=False, **kwargs)

    def assert_files(self, merged, name, subdir='merge', skip_files=None, skip_lines=None,
                     extra_dirs=tuple()):
        test_dir = self._test_dir(name, subdir)
        self._assert_files(merged, test_dir, skip_files=skip_files, skip_lines=skip_lines, extra_dirs=extra_dirs)
