from __future__ import absolute_import

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from http_request_randomizer.requests.parsers.UrlParser import UrlParser

__author__ = 'pgaref'


class TestBaseProxyParsers(unittest.TestCase):
    def setUp(self):
        self.normal_parser = UrlParser("proxy-test", "http://proxy-test.com", bandwidth_KBs=50)
        self.no_bdwidthParser = UrlParser("slow-proxy", "http://slow-proxy.com")

    def test_normal_parser(self):
        self.assertEqual(self.normal_parser.get_url(), "http://proxy-test.com", "incorrect parser URL")
        self.assertEqual(self.normal_parser.get_min_bandwidth(), 50, "incorrect parser bandwidth")

    def test_no_bandwidth_parser(self):
        self.assertEqual(self.no_bdwidthParser.get_url(), "http://slow-proxy.com", "incorrect parser URL")
        self.assertEqual(self.no_bdwidthParser.get_min_bandwidth(), 150, "incorrect parser bandwidth")


if __name__ == '__main__':
    unittest.main()
