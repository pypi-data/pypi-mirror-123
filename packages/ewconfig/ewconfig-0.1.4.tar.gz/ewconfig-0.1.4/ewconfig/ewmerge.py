from argparse import ArgumentParser
from logging import getLogger
from os import rmdir
from os.path import isfile
from shutil import move, rmtree

from .lib.args import ParagraphHelpFormatter, add_version_args
from .lib.file import assert_dir, tmp_dir, assert_empty_dir
from .lib.filter import Filter
from .lib.log import add_log_args, make_log_from_args
from .lib.markdown import add_md_help_argument
from .merge.chan import merge_filtered_chan
from .merge.prefer import Prefer
from .merge.rest import copy_rest
from .merge.sac import merge_sac
from .stationxml2ew import add_stationxml2ew_args, main_single

log = getLogger(__name__)


def expand_xml(file, drop_comment=False, m_to_nm=1, geophone=False,
               lo_precision=False, default_response=None,
               sta_filter=Filter('Station'), chan_filter=Filter('Channel'), date=None):
    if isfile(file):
        log.warning(f'Treating {file} as a station.xml file and calling stationxml2ew')
        dir = tmp_dir()
        main_single(file, dir=dir, drop_comment=drop_comment, m_to_nm=m_to_nm, geophone=geophone,
                    lo_precision=lo_precision, default_response=default_response,
                    sta_filter=sta_filter, chan_filter=chan_filter, date=date)
        log.debug(f'Expanded {file} into {dir}')
        return dir, file
    else:
        return file, False


def prepare_dirs(old, news, merged=None, backup=None, force=False):
    # we always have a merged, even if --force (when it is copied to old later)
    old = assert_dir(old, 'Old directory (--old)')
    news = [(assert_dir(new, 'New directory (--new)'), delete) for new, delete in news]
    merged = merged or tmp_dir()
    merged = assert_empty_dir(merged, 'Merge directory (--merge)')
    if force:
        if backup == 'NONE':
            log.warning('No backup (--backup NONE)')
            backup = None
        else:
            backup = backup or tmp_dir()
            backup = assert_empty_dir(backup, 'Backup directory (--backup)')
            rmdir(backup)  # so that move creates this directory instead of copying to inside it
    return old, news, merged, backup


def main(old, news, merged=None, backup=None, force=False, prefer=Prefer.CHECK, sort=True,
         drop_comment=False, m_to_nm=1, geophone=False, lo_precision=False, default_response=None,
         sta_filter=Filter('Station'), chan_filter=Filter('Channel'), date=None):
    if force:
        if merged: raise Exception('Do not specify --merged with --force')
    else:
        if backup: raise Exception('Do not specify --backup without --force')
    news = [expand_xml(new, drop_comment=drop_comment, m_to_nm=m_to_nm, geophone=geophone,
                       lo_precision=lo_precision, default_response=default_response,
                       sta_filter=sta_filter, chan_filter=chan_filter, date=date) for new in news]
    old, news, merged, backup = prepare_dirs(old, news, merged=merged, backup=backup, force=force)
    for new, delete in news:
        log.info(f'Processing directory {new}')
        merge_sac(old, new, merged, prefer)
        merge_filtered_chan(old, new, merged, prefer, sort)
        if delete:
            log.debug(f'Deleting temporary {new} (where {delete} was expanded)')
            rmtree(new)
    copy_rest(old, merged)
    if force:
        if backup:
            log.info(f'Moving {old} to {backup} (creating backup)')
            move(old, backup)
        else:
            log.warning(f'Deleting {old} (--backup NONE)')
            rmtree(old)
        log.info(f'Moving {merged} to {old} (overwriting old)')
        move(merged, old)
        return backup
    else:
        return merged


def main_args():
    try:
        parser = ArgumentParser(prog='ewmerge', add_help=False,
                                formatter_class=ParagraphHelpFormatter,
                                description='''A program to merge two EW configurations 
(at --old and --new) selecting entries based on NSCLs.

In the final output, files in the eqk/response and chan sub-directories are merged / filtered 
using NSCLs as described above.  All other files and directories are taken from --old.

If --force is NOT given then the output is saved to a new directory, whose path is printed
to stdout.  This path can be specified with --merged.

If --force is given then the output replaces the --old directory.  A copy of the initial data 
in --old is made and the path to this directory printed to stdout.  This path can be specified with 
--backup.

If you really want to overwrite existing with no backup data use "--force --backup NONE".
''')
        group = parser.add_argument_group(title='Merge parameters')
        group.add_argument('--old', required=True, help='Directory for old config.')
        group.add_argument('--new', required=True, nargs='+',
                           help='Directory(s) or XML file(s) for new config.  '
                                'XML files are expanded by stationxml2ew (see parameters below).')
        prefer = group.add_mutually_exclusive_group()
        prefer.add_argument('--prefer-old', action='store_const', dest='prefer', const=Prefer.OLD,
                            help='If a NSCL is present in old and new, use the old entries '
                                 '(default is to require identical entries).')
        prefer.add_argument('--prefer-new', action='store_const', dest='prefer', const=Prefer.NEW,
                            help='If a NSCL is present in old and new, use the new entries.')
        group.set_defaults(prefer=Prefer.CHECK)
        group.add_argument('--force', action='store_true', help='Replace old directory with merged.')
        group.add_argument('--backup', help='Backup directory for old config when replacing (if --force).')
        group.add_argument('--merged', help='Destination directory for merged config (if not --force).')
        group.add_argument('--no-sort', default=False, action='store_true',
                            help='Don\'t sort NSCLs in output.')
        group.add_argument('-h', action='help', help='Show this help message and exit.')
        add_version_args(group)
        add_md_help_argument(group)
        add_log_args(group)
        group = parser.add_argument_group(title='XML expansion parameters (passed to stationxml2ew)')
        add_stationxml2ew_args(group)
        args = parser.parse_args()
        make_log_from_args(parser.prog, args)
        if (args.force and args.merged) or (not args.force and args.backup):
            raise Exception('Use --merged with --force and --backup without')
        output = main(old=args.old, news=args.new, merged=args.merged, backup=args.backup,
                      force=args.force, prefer=args.prefer, sort=(not args.no_sort),
                      drop_comment=args.drop_comment, m_to_nm=args.nano, geophone=args.geophone,
                      default_response=args.default_response, date=args.date,
                      sta_filter=Filter('Station', includes=args.include_sta, excludes=args.exclude_sta),
                      chan_filter=Filter('Channel', includes=args.include_chan, excludes=args.exclude_chan))
        if output:  # None if --backup NONE
            print(output)
    except Exception as e:
        log.critical(e)
        exit(1)


if __name__ == '__main__':
    main_args()
