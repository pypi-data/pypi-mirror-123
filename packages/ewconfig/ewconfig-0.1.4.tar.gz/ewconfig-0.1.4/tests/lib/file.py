from logging import getLogger
from os.path import dirname, abspath, join

log = getLogger(__name__)


def project_root():
    own_dir = dirname(__file__)
    log.debug(f'lib located in {own_dir}')
    return abspath(join(own_dir, '..', '..', '..'))


