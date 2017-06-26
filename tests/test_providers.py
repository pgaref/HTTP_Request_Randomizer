from __future__ import absolute_import

import unittest
import sys
import os
from httmock import HTTMock

sys.path.insert(0, os.path.abspath('.'))

from tests.mocks import free_proxy_mock, proxy_for_eu_mock, rebro_weebly_mock, samair_mock
from tests.mocks import free_proxy_expected, proxy_for_eu_expected, rebro_weebly_expected, samair_expected
from http_request_randomizer.requests.parsers.FreeProxyParser import FreeProxyParser
from http_request_randomizer.requests.parsers.ProxyForEuParser import ProxyForEuParser
from http_request_randomizer.requests.parsers.RebroWeeblyParser import RebroWeeblyParser
from http_request_randomizer.requests.parsers.SamairProxyParser import SamairProxyParser

__author__ = 'pgaref'


class TestProxyProviders(unittest.TestCase):

    def test_FreeProxyParser(self):
        with HTTMock(free_proxy_mock):
            proxy_provider = FreeProxyParser('FreeProxy', 'http://free-proxy-list.net')
            proxy_list = proxy_provider.parse_proxyList()
            proxy_list_addr = []
            for proxy in proxy_list:
                proxy_list_addr.append(proxy.getAddress())
        self.assertEqual(proxy_list_addr, free_proxy_expected)

    def test_ProxyForEuParser(self):
        with HTTMock(proxy_for_eu_mock):
            proxy_provider = ProxyForEuParser('ProxyForEU', 'http://proxyfor.eu/geo.php', 1.0)
            proxy_list = proxy_provider.parse_proxyList()
            proxy_list_addr = []
            for proxy in proxy_list:
                proxy_list_addr.append(proxy.getAddress())
        self.assertEqual(proxy_list_addr, proxy_for_eu_expected)

    def test_RebroWeeblyParser(self):
        with HTTMock(rebro_weebly_mock):
            proxy_provider = RebroWeeblyParser('ReBro', 'http://rebro.weebly.com')
            proxy_list = proxy_provider.parse_proxyList()
            proxy_list_addr = []
            for proxy in proxy_list:
                proxy_list_addr.append(proxy.getAddress())
        self.assertEqual(proxy_list_addr, rebro_weebly_expected)

    def test_SemairProxyParser(self):
        with HTTMock(samair_mock):
            proxy_provider = SamairProxyParser('Samair', 'http://www.samair.ru/proxy/time-01.htm')
            proxy_list = proxy_provider.parse_proxyList()
            proxy_list_addr = []
            for proxy in proxy_list:
                proxy_list_addr.append(proxy.getAddress())
        self.assertEqual(proxy_list_addr, samair_expected)


if __name__ == '__main__':
    unittest.main()
