from filecmp import cmp
from logging import getLogger
from os import listdir, makedirs
from os.path import abspath, normpath, expanduser, exists, isdir
from tempfile import mkdtemp

log = getLogger(__name__)


def assert_dir(dir, name=None, create=False):
    dir = clean_path(dir)
    if not exists(dir):
        if create:
            log.debug(f'Creating {dir}')
            makedirs(dir)
        else:
            raise Exception(f'{dir} {"(" + name + ") " if name else ""}does not exist')
    if not isdir(dir):
        raise Exception(f'{dir} ({name}) is not a directory')
    log.debug(f'{dir} exists and is a directory')
    return dir


def tmp_dir():
    # note this does not delete or clean up the directory, it just creates it
    return mkdtemp(prefix='ewconfig')


def assert_empty_dir(dir, name=None):
    dir = assert_dir(dir, name=name, create=True)
    if listdir(dir):
        raise Exception(f'{dir} {"(" + name + ") " if name else ""}is not empty')
    log.debug(f'{dir} is empty')
    return dir


def clean_path(path):
    return abspath(normpath(expanduser(path)))


def assert_equal_contents(file1, file2):
    if not cmp(file1, file2, shallow=False):
        raise Exception(f'Files {file1} and {file2} differ')
    else:
        log.debug(f'Compared {file1} and {file2}')
