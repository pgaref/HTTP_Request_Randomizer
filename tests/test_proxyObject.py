from __future__ import absolute_import

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('.'))

from http_request_randomizer.requests.proxy.ProxyObject import AnonymityLevel, ProxyObject


class TestProxyObject(unittest.TestCase):

    def test_ProxyObjectSimple(self):
        src = 'Test'
        ip = '127.0.0.1'
        port = '8080'
        po = ProxyObject(src, ip, port, AnonymityLevel.UNKNOWN)
        self.assertEqual(po.source, src)
        self.assertEqual(po.ip, ip)
        self.assertEqual(po.port, port)
        self.assertEqual(po.get_address(), "{0}:{1}".format(ip, port))

    def test_AnonymityLevels(self):
        self.assertTrue(AnonymityLevel.UNKNOWN.value == 0)
        self.assertTrue(AnonymityLevel.TRANSPARENT.value == 1)
        self.assertTrue(AnonymityLevel.ANONYMOUS.value == 2)
        self.assertTrue(AnonymityLevel.ELITE.value == 3)
        self.assertTrue(len(AnonymityLevel) == 4)  # Enum values

    def test_UnknownEnumLevel(self):
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel.get('unknown'))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel.get('none'))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel.get('bad'))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel.get(''))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel.get('*'))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel.get('??'))

    def test_TransparentEnumLevel(self):
        self.assertEqual(AnonymityLevel.TRANSPARENT, AnonymityLevel.get('transparent'))
        self.assertEqual(AnonymityLevel.TRANSPARENT, AnonymityLevel.get('transparent proxy'))
        self.assertEqual(AnonymityLevel.TRANSPARENT, AnonymityLevel.get('LOW'))

    def test_AnonymousEnumLevel(self):
        self.assertEqual(AnonymityLevel.ANONYMOUS, AnonymityLevel.get('anonymous'))
        self.assertEqual(AnonymityLevel.ANONYMOUS, AnonymityLevel.get('anonymous proxy'))
        self.assertEqual(AnonymityLevel.ANONYMOUS, AnonymityLevel.get('high-anonymous'))

    def test_EliteEnumLevel(self):
        self.assertEqual(AnonymityLevel.ELITE, AnonymityLevel.get('elite'))
        self.assertEqual(AnonymityLevel.ELITE, AnonymityLevel.get('elite proxy'))
        self.assertEqual(AnonymityLevel.ELITE, AnonymityLevel.get('HIGH'))
        self.assertEqual(AnonymityLevel.ELITE, AnonymityLevel.get('Elite & Anonymous'))


if __name__ == '__main__':
    unittest.main()
