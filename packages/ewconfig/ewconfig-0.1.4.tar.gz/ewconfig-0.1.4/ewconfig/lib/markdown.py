
# https://chromium.googlesource.com/catapult/+/refs/heads/master/devil/devil/utils/markdown.py
# https://chromium.googlesource.com/catapult/+/refs/heads/master/LICENSE

# 2021-03-25 - acooke - removed unused code that had deprecated imports.
#                     - escaped * in help text

# Copyright 2015 The Chromium Authors. All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of catapult nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import os
import re

from .args import ParagraphHelpFormatter

# A markdown code block template: https://goo.gl/9EsyRi

_CODE_BLOCK_FORMAT = '''```{language}
{code}
```
'''
_DEVIL_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..'))


def md_bold(raw_text):
    """Returns markdown-formatted bold text."""
    return '**%s**' % md_escape(raw_text, characters='*')


def md_code(raw_text, language):
    """Returns a markdown-formatted code block in the given language."""
    return _CODE_BLOCK_FORMAT.format(
        language=language or '', code=md_escape(raw_text, characters='`'))


def md_escape(raw_text, characters='*_'):
    """Escapes * and _."""

    def escape_char(m):
        return '\\%s' % m.group(0)

    pattern = '[%s]' % re.escape(characters)
    return re.sub(pattern, escape_char, raw_text)


def md_heading(raw_text, level):
    """Returns markdown-formatted heading."""
    adjusted_level = min(max(level, 0), 6)
    return '%s%s%s' % ('#' * adjusted_level, ' ' if adjusted_level > 0 else '',
                       raw_text)


def md_inline_code(raw_text):
    """Returns markdown-formatted inline code."""
    return '`%s`' % md_escape(raw_text, characters='`')


def md_italic(raw_text):
    """Returns markdown-formatted italic text."""
    return '*%s*' % md_escape(raw_text, characters='*')


def md_link(link_text, link_target):
    """returns a markdown-formatted link."""
    return '[%s](%s)' % (md_escape(link_text, characters=']'),
                         md_escape(link_target, characters=')'))


class MarkdownHelpFormatter(ParagraphHelpFormatter):
    """A really bare-bones argparse help formatter that generates valid markdown.
    This will generate something like:
    usage
    # **section heading**:
    ## **--argument-one**
    ```
    argument-one help text
    ```
    """

    # override
    def _format_usage(self, usage, actions, groups, prefix):
        usage_text = super(MarkdownHelpFormatter, self)._format_usage(
            usage, actions, groups, prefix)
        return md_code(usage_text, language=None)

    # override
    def format_help(self):
        self._root_section.heading = md_heading(self._prog, level=1)
        return md_escape(super(MarkdownHelpFormatter, self).format_help(), characters='*')

    # override
    def start_section(self, heading):
        super(MarkdownHelpFormatter, self).start_section(
            md_heading(heading, level=2))

    # override
    def _format_action(self, action):
        lines = []
        action_header = self._format_action_invocation(action)
        lines.append(md_heading(action_header, level=3))
        if action.help:
            lines.append(md_code(self._expand_help(action), language=None))
        lines.extend(['', ''])
        return '\n'.join(lines)


class MarkdownHelpAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 **kwargs):
        super(MarkdownHelpAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        parser.formatter_class = MarkdownHelpFormatter
        parser.print_help()
        parser.exit()


def add_md_help_argument(parser):
    """Adds --md-help to the given argparse.ArgumentParser.
    Running a script with --md-help will print the help text for that script
    as valid markdown.
    Args:
      parser: The ArgumentParser to which --md-help should be added.
    """
    parser.add_argument(
        '--md-help',
        action=MarkdownHelpAction,
        help='Print Markdown-formatted help text and exit.')

