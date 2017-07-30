from __future__ import absolute_import

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from http_request_randomizer.requests.proxy.ProxyObject import AnonymityLevel


class TestProxyObject(unittest.TestCase):

    def test_AnonymityLevels(self):
        self.assertTrue(AnonymityLevel.UNKNOWN.value == 0)
        self.assertTrue(AnonymityLevel.TRANSPARENT.value == 1)
        self.assertTrue(AnonymityLevel.ANONYMOUS.value == 2)
        self.assertTrue(AnonymityLevel.ELITE.value == 3)
        self.assertTrue(len(AnonymityLevel) == 4)  # Enum values

    def test_UnknownEnumLevel(self):
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel('unknown'))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel('none'))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel('bad'))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel(''))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel('*'))
        self.assertEqual(AnonymityLevel.UNKNOWN, AnonymityLevel('??'))

    def test_TransparentEnumLevel(self):
        self.assertEqual(AnonymityLevel.TRANSPARENT, AnonymityLevel('transparent'))
        self.assertEqual(AnonymityLevel.TRANSPARENT, AnonymityLevel('transparent proxy'))
        self.assertEqual(AnonymityLevel.TRANSPARENT, AnonymityLevel('LOW'))

    def test_AnonymousEnumLevel(self):
        self.assertEqual(AnonymityLevel.ANONYMOUS, AnonymityLevel('anonymous'))
        self.assertEqual(AnonymityLevel.ANONYMOUS, AnonymityLevel('anonymous proxy'))
        self.assertEqual(AnonymityLevel.ANONYMOUS, AnonymityLevel('high-anonymous'))

    def test_EliteEnumLevel(self):
        self.assertEqual(AnonymityLevel.ELITE, AnonymityLevel('elite'))
        self.assertEqual(AnonymityLevel.ELITE, AnonymityLevel('elite proxy'))
        self.assertEqual(AnonymityLevel.ELITE, AnonymityLevel('HIGH'))


if __name__ == '__main__':
    unittest.main()
