from glob import glob
from logging import getLogger
from os.path import join, basename, sep
from re import compile, escape
from shutil import copy

from .merge import merge
from ..lib.file import assert_dir, assert_equal_contents

log = getLogger(__name__)


def merge_sac(old, new, merged, prefer):
    merge(old, new, merged, prefer, parse_sac, assert_equal_contents, write_sac)


def parse_sac(dir):
    return {nscl: path for nscl, path in glob_sac(dir)}


def glob_sac(dir):
    if dir:
        eqk_response = assert_dir(join(dir, 'eqk', 'response'))
        for file in glob(join(eqk_response, '*.sac')):
            match = NSCL_sac.match(file)
            if match:
                yield match.group(1), file
            else:
                log.warning(f'Could not parse {file}')


def write_sac(merged, nscls_map):
    dest_eqk_response = assert_dir(join(merged, 'eqk', 'response'), create=True)
    for nscl, path in nscls_map.items():
        log.debug(f'Copying {path} for {nscl} to {dest_eqk_response}')
        copy(path, join(dest_eqk_response, basename(path)))


NSCL_sac = compile(r'^.*' + escape(sep) + r'([A-Z0-9]+\.[A-Z0-9]+\.[A-Z0-9]+\.[-A-Z0-9]+)\.sac$')