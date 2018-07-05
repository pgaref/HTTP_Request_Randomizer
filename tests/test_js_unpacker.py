import unittest
import sys
import os
from httmock import HTTMock

from http_request_randomizer.requests.parsers.js.UnPacker import JsUnPacker
from tests.mocks import prem_js_mock

sys.path.insert(0, os.path.abspath('.'))

__author__ = 'pgaref'


class TestJS(unittest.TestCase):

    def test_js_unpacker(self):
        with HTTMock(prem_js_mock):
            JsUnPacker('https://www.premproxy.com/js/test.js')


if __name__ == '__main__':
    unittest.main()