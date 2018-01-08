from __future__ import absolute_import

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('.'))
from http_request_randomizer.requests.runners.proxyList import ProxyList, create_parser


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.proxyList = ProxyList()
        self.parser = create_parser(self.proxyList)

    def test_ParserSource(self):
        parsed = self.parser.parse_args(['-s', 'freeproxy'])
        self.assertEqual(parsed.sources, ['freeproxy'])

        parsed = self.parser.parse_args(['-s', 'freeproxy', 'all', 'proxyforeu'])
        self.assertEqual(parsed.sources, ['freeproxy', 'all', 'proxyforeu'])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-s'])
            self.parser.parse_args(['-s', 'blah'])

    def test_ParserList(self):
        parsed = self.parser.parse_args(['-ls', 'providers'])
        self.assertEqual(parsed.list, ['providers'])

        parsed = self.parser.parse_args(['-ls', 'agents'])
        self.assertEqual(parsed.list, ['agents'])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-ls'])
            self.parser.parse_args(['-ls', 'test'])


if __name__ == '__main__':
    unittest.main()

