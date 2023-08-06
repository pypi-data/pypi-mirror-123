from abc import ABC
from logging import getLogger
from os import makedirs
from os.path import join, exists

log = getLogger(__name__)


class BaseParser(ABC):

    def __init__(self, file):
        self._file = file

    def read(self, dir):
        path = join(dir, 'chan', self._file)
        if exists(path):
            log.debug(f'Reading {path}')
            with open(path, 'r') as src:
                self._read(src)
        else:
            log.warning(f'Could not find {path}')

    def _read(self, file):
        raise NotImplementedError('_read')

    def add(self, new):
        raise NotImplementedError('add')

    def write(self, merged):
        dir = join(merged, 'chan')
        if not exists(dir):
            makedirs(dir)
        path = join(dir, self._file)
        log.info(f'Writing {path}')
        with open(path, 'w') as file:
            self._write(file)

    def _write(self, file):
        raise NotImplementedError('_write')

