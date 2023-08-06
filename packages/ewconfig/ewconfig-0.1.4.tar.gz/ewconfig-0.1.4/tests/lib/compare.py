from itertools import zip_longest
from logging import getLogger
from os import listdir
from os.path import join, exists
from re import search, sub, compile

log = getLogger(__name__)


class Compare:

    def _test_dir(self, name, subdir=None):
        raise NotImplementedError('_test_dir')

    def _assert_files(self, dest_dir, test_dir, rdseed=False, skip_files=None, skip_lines=None, extra_dirs=tuple()):
        skip_files_all = tuple() if rdseed else (r'rdseed\.err_log', r'SAC_PZs_.*')
        if skip_files: skip_files_all = skip_files_all + skip_files
        skip_lines_all = (r'^Date', r'^CREATED', r'^\*')
        if skip_lines: skip_lines_all = skip_lines_all + skip_lines
        for subdir in ('chan', join('eqk', 'response'), *extra_dirs):
            self.__assert_dirs(join(test_dir, subdir), join(dest_dir, subdir), skip_files=skip_files_all)
            self.__assert_dirs(join(dest_dir, subdir), join(test_dir, subdir), contents=True,
                               skip_files=skip_files_all, skip_lines=skip_lines_all)

    def __assert_dirs(self, dir1, dir2, contents=False, skip_files=tuple(), skip_lines=tuple()):
        for file in listdir(dir1):
            if any(search(skip, file) for skip in skip_files):
                log.debug(f'Skipping {file}')
            else:
                path1 = join(dir1, file)
                path2 = join(dir2, file)
                self.assertTrue(exists(path2), f'{file} from {dir1} missing from {dir2}')
                if contents:
                    with open(path1) as file1, open(path2) as file2:
                        lines1 = [line for line in file1 if not any(search(skip, line) for skip in skip_lines)]
                        lines2 = [line for line in file2 if not any(search(skip, line) for skip in skip_lines)]
                        for line1, line2 in zip_longest(lines1, lines2):
                            line1 = self.__fix_negative_zero(line1)
                            line2 = self.__fix_negative_zero(line2)
                            if line1 and line2 and 'CONSTANT' in line1 and 'CONSTANT' in line2:
                                self.__compare_constants(line1, line2)
                            else:
                                self.assertEqual(line1, line2, f'from {file} ({dir1} v {dir2})')

    def __fix_negative_zero(self, line):
        # we don't care about -0 being different to 0
        if line:
            return sub(r'\-0\.000000e\+00', r'0.000000e+00', line)
        else:
            return line

    def __compare_constants(self, line1, line2):
        # need to drop some precision here.  suspect it is ok.
        CONSTANT = compile(r'CONSTANT\s+(\S*)\s*(?:\*.*)?')  # optional group is trailing comment (units)
        constant1 = '%.4e' % float(CONSTANT.match(line1).group(1))
        constant2 = '%.4e' % float(CONSTANT.match(line2).group(1))
        self.assertEqual(constant1, constant2, f'{line1} / {line2}')
