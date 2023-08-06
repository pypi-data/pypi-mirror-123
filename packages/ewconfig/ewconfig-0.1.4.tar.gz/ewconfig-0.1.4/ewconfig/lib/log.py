
from logging import getLogger, DEBUG, Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
from os.path import join, exists

# need to save these to close logging
# (so we can restart at different levels for different tests)
__FILE_HANDLER = None
__STDERR_HANDLER = None


def make_log(progname, verbosity, log_verbosity=4, path=None):

    global __FILE_HANDLER, __STDERR_HANDLER

    level = 10 * (6 - verbosity)
    log_level = 10 * (6 - log_verbosity)

    if not getLogger(progname).handlers:

        sacpz2ew_log = getLogger('ewconfig')
        sacpz2ew_log.setLevel(DEBUG)
        test_log = getLogger('tests')
        test_log.setLevel(DEBUG)
        # capture logging from an executing module, if one exists
        main_log = getLogger('__main__')
        main_log.setLevel(DEBUG)

        if path:
            filepath = join(path, progname + '.log')
            old_log = exists(filepath)
            file_formatter = Formatter('%(levelname)-8s %(asctime)s: %(message)s')
            try:
                __FILE_HANDLER = RotatingFileHandler(filepath, backupCount=10)
            except Exception as e:
                raise Exception(f'\nThere was an error trying to create logs at {filepath} '
                                f'and so logging failed to initialise.'
                                f'\n\n({e})\n')
            # we rollover so that the new log goes to a new file
            # since we specify no size limit the entire load goes into a single log
            if old_log: __FILE_HANDLER.doRollover()
            __FILE_HANDLER.setLevel(log_level)
            __FILE_HANDLER.setFormatter(file_formatter)
            sacpz2ew_log.addHandler(__FILE_HANDLER)
            test_log.addHandler(__FILE_HANDLER)
            main_log.addHandler(__FILE_HANDLER)

        if verbosity:
            stderr_formatter = Formatter('%(levelname)8s: %(message)s')
            __STDERR_HANDLER = StreamHandler()
            __STDERR_HANDLER.setLevel(level)
            __STDERR_HANDLER.setFormatter(stderr_formatter)
            test_log.addHandler(__STDERR_HANDLER)
            sacpz2ew_log.addHandler(__STDERR_HANDLER)
            main_log.addHandler(__STDERR_HANDLER)


def clear_log():
    global __FILE_HANDLER, __STDERR_HANDLER
    if __FILE_HANDLER or __STDERR_HANDLER:
        for handler in __FILE_HANDLER, __STDERR_HANDLER:
            for log in 'ewconfig', 'tests', '__main__':
                getLogger(log).removeHandler(handler)
        __FILE_HANDLER.close()
        __FILE_HANDLER = None
        __STDERR_HANDLER = None


def add_log_args(parser):
    parser.add_argument('-v', '--verbosity', default=4, type=int, metavar='INTEGER',
                        help='Log level (0: silent, 5: debug)')


def make_log_from_args(prog, args):
    make_log(prog, args.verbosity)
