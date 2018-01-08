from __future__ import absolute_import

import os
import sys
import unittest

from http_request_randomizer.requests.runners.proxyList import ProxyList, create_parser

sys.path.insert(0, os.path.abspath('.'))

__author__ = 'pgaref'


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.proxyList = ProxyList()
        self.parser = create_parser(self.proxyList)

    def test_parser_source(self):
        parsed = self.parser.parse_args(['-s', 'freeproxy'])
        self.assertEqual(parsed.source, ['freeproxy'])

        parsed = self.parser.parse_args(['-s', 'freeproxy', 'all', 'proxyforeu'])
        self.assertEqual(parsed.source, ['freeproxy', 'all', 'proxyforeu'])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-s'])
            self.parser.parse_args(['-s', 'blah'])

    def test_parser_output(self):
        # default
        parsed = self.parser.parse_args(['-s', 'all'])
        self.assertEqual(parsed.outfile, sys.stdout)

        parsed = self.parser.parse_args(['-s', 'all', '-o', 'out.txt'])
        self.assertEqual(parsed.outfile.name, 'out.txt')

    def test_parser_timeout(self):
        # default
        parsed = self.parser.parse_args(['-s', 'all'])
        self.assertEqual(parsed.timeout, 1)

        parsed = self.parser.parse_args(['-s', 'all', '-t', '20'])
        self.assertEqual(parsed.timeout, 20)

        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-s', 'all', '-t', 't'])

    def test_parser_bandwidth(self):
        # default
        parsed = self.parser.parse_args(['-s', 'all'])
        self.assertEqual(parsed.bandwidth, 10)

        parsed = self.parser.parse_args(['-s', 'all', '-bw', '500'])
        self.assertEqual(parsed.bandwidth, 500)

        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-s', 'all', '-bw', 'b'])


if __name__ == '__main__':
    unittest.main()
