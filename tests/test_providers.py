from __future__ import absolute_import

import unittest
import sys
import os
from httmock import HTTMock

sys.path.insert(0, os.path.abspath('.'))

from tests.mocks import free_proxy_mock,proxy_for_eu_mock, rebro_weebly_mock, samair_mock
from http_request_randomizer.requests.parsers.FreeProxyParser import FreeProxyParser
from http_request_randomizer.requests.parsers.ProxyForEuParser import ProxyForEuParser
from http_request_randomizer.requests.parsers.RebroWeeblyParser import RebroWeeblyParser
from http_request_randomizer.requests.parsers.SamairProxyParser import SamairProxyParser

__author__ = 'pgaref'


class TestProxyProviders(unittest.TestCase):

    def test_FreeProxyParser(self):
        with HTTMock(free_proxy_mock):
            proxy_provider = FreeProxyParser('http://free-proxy-list.net')
            proxy_list = proxy_provider.parse_proxyList()
        self.assertEqual(proxy_list, ['http://138.197.136.46:3128', 'http://177.207.75.227:8080'])

    def test_ProxyForEuParser(self):
        with HTTMock(proxy_for_eu_mock):
            proxy_provider = ProxyForEuParser('http://proxyfor.eu/geo.php', 1.0)
            proxy_list = proxy_provider.parse_proxyList()
        self.assertEqual(proxy_list, ['http://107.151.136.222:80', 'http://37.187.253.39:8115'])

    def test_RebroWeeblyParser(self):
        with HTTMock(rebro_weebly_mock):
            proxy_provider = RebroWeeblyParser('http://rebro.weebly.com')
            proxy_list = proxy_provider.parse_proxyList()
        self.assertEqual(proxy_list, ['http://213.149.105.12:8080', 'http://119.188.46.42:8080'])

    def test_SemairProxyParser(self):
        with HTTMock(samair_mock):
            proxy_provider = SamairProxyParser('http://www.samair.ru/proxy/time-01.htm')
            proxy_list = proxy_provider.parse_proxyList()
        self.assertEqual(proxy_list, ['http://191.252.61.28:80', 'http://167.114.203.141:8080'])


if __name__ == '__main__':
    unittest.main()
