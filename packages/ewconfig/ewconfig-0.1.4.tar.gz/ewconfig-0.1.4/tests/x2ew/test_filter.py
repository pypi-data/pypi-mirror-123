from unittest import TestCase

from ewconfig.lib.filter import Filter
from ..lib.log import LogMixin


class TestFilter(LogMixin, TestCase):

    stderr_verbosity = 5

    def test_literal(self):
        self.assertFilter(['a', 'b'], ['b', 'c'], ['a', 'b', 'c'], ['a'])

    def test_default(self):
        self.assertFilter([], ['b', 'c'], ['a', 'b', 'c'], ['a'])

    def test_pattern(self):
        self.assertFilter(['?x*'], ['*z'], ['a', 'x', 'xx', 'xxxx', 'xxxz'], ['xx', 'xxxx'])

    def assertFilter(self, include, exclude, all, target):
        filter = Filter('test', include, exclude)
        result = list(filter(all))
        self.assertEqual(target, result)
