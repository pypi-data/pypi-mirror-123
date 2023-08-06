from itertools import zip_longest
from logging import getLogger
from os import makedirs, chdir, listdir
from os.path import join, exists
from re import search, sub, compile
from shutil import rmtree
from subprocess import run

from ewconfig.lib.file import tmp_dir
from .compare import Compare
from .file import project_root

log = getLogger(__name__)


class MainMixin(Compare):

    def _src_dir(self, name):
        return join(project_root(), 'data', name.lower())

    def _test_dir(self, name):
        return join(self._src_dir(name), 'x2ew')

    def _dest_dir(self, name):
        return join(tmp_dir(), name.lower())

    def _create_dest_dir(self, name):
        dest_dir = self._dest_dir(name)
        rmtree(dest_dir, ignore_errors=True)
        makedirs(dest_dir)
        chdir(dest_dir)
        return dest_dir

    def run_sac2ew(self, name):
        from ewconfig.sacpz2ew import main
        dest_dir = self._create_dest_dir(name)
        src_dir = self._src_dir(name)
        log.info(f'Running with input from {src_dir} and output to {dest_dir}')
        log.debug('Calling rdseed')
        run(['rdseed', '-pf', join(src_dir, name + '.dataless')])
        main(dest_dir)
        return dest_dir

    def run_xml2ew(self, name, **kwargs):
        from ewconfig.stationxml2ew import main_single
        dest_dir = self._create_dest_dir(name)
        src_dir = self._src_dir(name)
        log.info(f'Running with input from {src_dir} and output to {dest_dir}')
        main_single(join(src_dir, name + '.xml'), **kwargs)
        return dest_dir

    def assert_files(self, dest_dir, name, rdseed=False, skip_files=None, skip_lines=None):
        test_dir = self._test_dir(name)
        self._assert_files(dest_dir, test_dir, rdseed=rdseed, skip_files=skip_files, skip_lines=skip_lines)
