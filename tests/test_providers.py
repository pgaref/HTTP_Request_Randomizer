from __future__ import absolute_import

import unittest
import sys
import os
from httmock import HTTMock

sys.path.insert(0, os.path.abspath('.'))

from tests.mocks import free_proxy_mock, proxy_for_eu_mock, rebro_weebly_mock, prem_mock, sslproxy_mock
from tests.mocks import free_proxy_expected, proxy_for_eu_expected, rebro_weebly_expected, prem_expected, prem_js_mock, sslproxy_expected
from http_request_randomizer.requests.parsers.FreeProxyParser import FreeProxyParser
from http_request_randomizer.requests.parsers.ProxyForEuParser import ProxyForEuParser
from http_request_randomizer.requests.parsers.RebroWeeblyParser import RebroWeeblyParser
from http_request_randomizer.requests.parsers.PremProxyParser import PremProxyParser
from http_request_randomizer.requests.parsers.SslProxyParser import SslProxyParser

__author__ = 'pgaref'


class TestProxyProviders(unittest.TestCase):

    def test_FreeProxyParser(self):
        with HTTMock(free_proxy_mock):
            proxy_provider = FreeProxyParser('FreeProxy', 'http://free-proxy-list.net')
            proxy_list = proxy_provider.parse_proxyList()
            proxy_list_addr = []
            for proxy in proxy_list:
                proxy_list_addr.append(proxy.get_address())
        self.assertEqual(proxy_list_addr, free_proxy_expected)

    def test_ProxyForEuParser(self):
        with HTTMock(proxy_for_eu_mock):
            proxy_provider = ProxyForEuParser('ProxyForEU', 'http://proxyfor.eu/geo.php', 1.0)
            proxy_list = proxy_provider.parse_proxyList()
            proxy_list_addr = []
            for proxy in proxy_list:
                proxy_list_addr.append(proxy.get_address())
        self.assertEqual(proxy_list_addr, proxy_for_eu_expected)

    def test_RebroWeeblyParser(self):
        with HTTMock(rebro_weebly_mock):
            proxy_provider = RebroWeeblyParser('ReBro', 'http://rebro.weebly.com')
            proxy_list = proxy_provider.parse_proxyList()
            proxy_list_addr = []
            for proxy in proxy_list:
                proxy_list_addr.append(proxy.get_address())
        self.assertEqual(proxy_list_addr, rebro_weebly_expected)

    def test_PremProxyParser(self):
        with HTTMock(prem_js_mock, prem_mock):
            proxy_provider = PremProxyParser('Prem', 'https://www.premproxy.com')
            proxy_list = proxy_provider.parse_proxyList()
            proxy_list_addr = []
            for proxy in proxy_list:
                proxy_list_addr.append(proxy.get_address())
            for item in prem_expected:
                self.assertTrue(item in proxy_list_addr)

    def test_SslProxyParser(self):
        with HTTMock(sslproxy_mock):
            proxy_provider = SslProxyParser('SslProxy', 'https://www.sslproxies.org/')
            proxy_list = proxy_provider.parse_proxyList()
            proxy_list_addr = []
            for proxy in proxy_list:
                proxy_list_addr.append(proxy.get_address())
        self.assertEqual(proxy_list_addr, sslproxy_expected)

if __name__ == '__main__':
    unittest.main()
