from __future__ import absolute_import

import unittest
import sys
import os

from http_request_randomizer.requests.useragent.userAgent import UserAgentManager

sys.path.insert(0, os.path.abspath('.'))

__author__ = 'pgaref'


class TestBaseProxyParsers(unittest.TestCase):
    def setUp(self):
        agentsfile = os.path.join(os.path.dirname(__file__), '../http_request_randomizer/requests/data/user_agents.txt')
        self.uafile = UserAgentManager(file=agentsfile)
        self.uafake = UserAgentManager()

    def test_agent_size(self):
        self.assertTrue(self.uafile.get_len_user_agent() >= 899)
        self.assertIsNone(self.uafake.get_len_user_agent())

    def test_fist_user_agent(self):
        expected = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0"
        self.assertEqual(self.uafile.get_first_user_agent(), expected)
        self.assertIsNone(self.uafake.get_first_user_agent())

    def test_last_user_agent(self):
        expected = "Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.2.15 Version/10.0"
        self.assertEqual(self.uafile.get_last_user_agent(), expected)
        self.assertIsNone(self.uafake.get_last_user_agent())

    def test_random_user_agent(self):
        count = 0
        for i in range(1, 101):
            if self.uafile.get_random_user_agent() == self.uafile.get_random_user_agent():
                count = count + 1
        self.assertNotEqual(count, i)


if __name__ == '__main__':
    unittest.main()
