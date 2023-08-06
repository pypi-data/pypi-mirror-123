from logging import getLogger

from .prefer import Prefer

log = getLogger(__name__)


def merge(old, new, merged, prefer, parser, assert_eq, writer):
    '''
    This is a HOF that merges old and new data in to merged.  It assumes that parser returns
    a map from NSCL to some info that is used by assert_eq and writer.  Unfortunately it's only
    used by SAC files because it turns out that other files have extra info that we need to
    carry across.
    '''
    nscls_map = merge_nscls(old, new, prefer, parser, assert_eq)
    writer(merged, nscls_map)


def merge_nscls(old, new, prefer, parser, assert_eq):
    old_nscls_map = parser(old)
    new_nscls_map = parser(new)
    if prefer == Prefer.CHECK:
        nscls_map = check_duplicates(old_nscls_map, new_nscls_map, assert_eq)
    else:
        nscls_map = pick_duplicates(old_nscls_map, new_nscls_map, prefer)
    return nscls_map


def check_duplicates(old_nscls_map, new_nscls_map, assert_eq):
    for old_nscl, old_value in old_nscls_map.items():
        if old_nscl in new_nscls_map:
            assert_eq(old_value, new_nscls_map[old_nscl])
            del new_nscls_map[old_nscl]
    old_nscls_map.update(new_nscls_map)
    return old_nscls_map


def pick_duplicates(old_nscls_map, new_nscls_map, prefer):
    conflicts = set(old_nscls_map.keys()).intersection(new_nscls_map.keys())
    if conflicts:
        conflicts_str = ', '.join(conflicts)
        if prefer == Prefer.OLD:
            log.info(f'Will take {conflicts_str} from old config')
            new_nscls_map.update(old_nscls_map)
            return new_nscls_map
        else:
            log.info(f'Will take {conflicts_str} from new config')
            old_nscls_map.update(new_nscls_map)
            return old_nscls_map
    else:
        old_nscls_map.update(new_nscls_map)
        return old_nscls_map
