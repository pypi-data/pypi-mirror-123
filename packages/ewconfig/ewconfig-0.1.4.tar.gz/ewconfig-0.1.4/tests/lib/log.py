from io import StringIO
from logging import StreamHandler, getLogger

from sys import stderr

from ewconfig.lib.log import make_log, clear_log


class LogMixin:

    stderr_verbosity = 4

    def setUp(self):
        stderr_verbosity = self.stderr_verbosity
        print(file=stderr)  # sabotage unittest's assumptions about inline stderr printing
        make_log(self.__class__.__name__, stderr_verbosity, path='/tmp')
        # do super (and sibling) classes AFTER setting up logs
        super().setUp()

    def tearDown(self):
        super().tearDown()
        clear_log()


class CaptureLog:
    '''
    https://stackoverflow.com/a/63678561
    '''

    def __init__(self, name='ewconfig'):
        self.logger = getLogger(name)
        self.io = StringIO()
        self.sh = StreamHandler(self.io)
        self.out = ''

    def __enter__(self):
        self.logger.addHandler(self.sh)
        return self

    def __exit__(self, *exc):
        self.logger.removeHandler(self.sh)
        self.out = self.io.getvalue()

    def __repr__(self):
        return f'captured: "{self.out}"\n'
