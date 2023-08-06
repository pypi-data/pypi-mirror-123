from logging import getLogger
from shutil import copytree

log = getLogger(__name__)


def copy_rest(old, merged):
    log.info(f'Copying rest of {old} to {merged}')
    copytree(old, merged, ignore=_copy_filter(old), dirs_exist_ok=True)


def _copy_filter(old):

    def filter(dir, files):
        if dir == old and 'chan' in files:
            return ['chan']
        elif dir == 'eqk' and 'response' in files:
            return ['response']
        else:
            return []

    return filter
