from __future__ import absolute_import

import unittest
import sys
import os

from http_request_randomizer.requests.useragent.userAgent import UserAgentManager

sys.path.insert(0, os.path.abspath('.'))

__author__ = 'pgaref'


class TestBaseProxyParsers(unittest.TestCase):
    def setUp(self):
        self.ua = UserAgentManager()

    def test_agent_size(self):
        self.assertTrue(self.ua.get_len_user_agent() >= 899)

    def test_fist_user_agent(self):
        expected = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0"
        self.assertEquals(self.ua.get_first_user_agent(), expected)

    def test_last_user_agent(self):
        expected = "Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.2.15 Version/10.0"
        self.assertEquals(self.ua.get_last_user_agent(), expected)

    def test_random_user_agent(self):
        self.assertNotEqual(self.ua.get_random_user_agent(), self.ua.get_random_user_agent())


if __name__ == '__main__':
    unittest.main()
