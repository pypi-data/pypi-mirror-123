from argparse import SUPPRESS, HelpFormatter
from re import split


class ParagraphHelpFormatter(HelpFormatter):
    '''
    Preserve paragraphs in the description and epilog.
    '''

    def add_text(self, text):
        if text is not SUPPRESS and text is not None:
            for para in split(r'\n\s*\n', text):
                self._add_item(self._format_text, [para])


def add_version_args(parser):
    from .. import __version__
    parser.add_argument('-V', '--version', action='version', version=__version__,
                        help='Show program\'s version number and exit.')
