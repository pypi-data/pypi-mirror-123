from fnmatch import translate
from logging import getLogger
from re import compile

log = getLogger(__name__)


class Filter:

    def __init__(self, name, includes=None, excludes=None):
        '''
        Create a filter for <name> that includes patterns in <includes>
        and then excludes patterns in <excludes>.
        If <includes> is missing then all are initially included.
        If <excludes> is missing then none are excluded.
        Patterns are 'globs' as supported by fnmatch module.
        '''
        self.__name = name
        if isinstance(includes, str) or isinstance(excludes, str):
            raise Exception('Filter takes lists of includes and excludes')
        if not includes: includes = ['*']
        if not excludes: excludes = []
        self.__str = f'{name}: include ' + ','.join(includes)
        if excludes: self.__str += '; exclude ' + ','.join(includes)
        self.__includes = [compile(translate(include)) for include in includes]
        self.__excludes = [compile(translate(exclude)) for exclude in excludes]

    def __call__(self, items, key=None, quiet=False):
        logged = set()
        if not key: key = lambda x: x
        for item in items:
            value = key(item)
            if any(include.match(value) for include in self.__includes):
                if not any(exclude.match(value) for exclude in self.__excludes):
                    yield item
                else:
                    if value not in logged:
                        if not quiet: log.info(f'{self.__name} {value} was explicitly excluded')
                        logged.add(value)
            else:
                if value not in logged:
                    if not quiet: log.info(f'{self.__name} {value} was not included')
                    logged.add(value)

    def __str__(self):
        return self.__str

