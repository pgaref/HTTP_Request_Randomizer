from __future__ import absolute_import

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from http_request_randomizer.requests.parsers.FreeProxyParser import FreeProxyParser
from http_request_randomizer.requests.parsers.ProxyForEuParser import ProxyForEuParser
from http_request_randomizer.requests.parsers.RebroWeeblyParser import RebroWeeblyParser
from http_request_randomizer.requests.parsers.SamairProxyParser import SamairProxyParser

__author__ = 'pgaref'


class TestProxyProviders(unittest.TestCase):
    # def setUp(self):

    def test_FreeProxyParser(self):
        proxy_provider = FreeProxyParser('http://free-proxy-list.net')
        proxy_provider.parse_proxyList()

    def test_ProxyForEuParser(self):
        proxy_provider = ProxyForEuParser('http://proxyfor.eu/geo.php')
        proxy_provider.parse_proxyList()

    def test_RebroWeeblyParser(self):
        proxy_provider = RebroWeeblyParser('http://rebro.weebly.com')
        proxy_provider.parse_proxyList()

    # def test_SemairProxyParser(self):
    #     proxy_provider = SamairProxyParser('http://www.samair.ru/proxy/time-01.htm')
    #     proxy_provider.parse_proxyList()


if __name__ == '__main__':
    unittest.main()
