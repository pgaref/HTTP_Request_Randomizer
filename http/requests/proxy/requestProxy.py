import os
import sys

sys.path.insert(0, os.path.abspath('../../../../'))
from http.requests.parsers.freeproxyParser import freeproxyParser
from http.requests.parsers.proxyforeuParser import proxyforeuParser
from http.requests.parsers.rebroweeblyParser import rebroweeblyParser
from http.requests.parsers.samairproxyParser import semairproxyParser
from http.requests.useragent.userAgent import UserAgentManager
import requests
from requests.exceptions import ConnectionError
from requests.exceptions import ChunkedEncodingError
import random
import time
from requests.exceptions import ReadTimeout

__author__ = 'pgaref'


class RequestProxy:
    def __init__(self, web_proxy_list=[], sustain=False, debug=True):
        self.userAgent = UserAgentManager()

        #####
        # Each of the classes below implements a specific URL Parser
        #####
        parsers = []
        parsers.append(freeproxyParser('http://free-proxy-list.net'))
        parsers.append(proxyforeuParser('http://proxyfor.eu/geo.php', 100.0))
        parsers.append(rebroweeblyParser('http://rebro.weebly.com/proxy-list.html'))
        parsers.append(semairproxyParser('http://www.samair.ru/proxy/time-01.htm'))

        print "=== Initialized Proxy Parsers ==="
        for i in range(len(parsers)):
            print "\t {0}".format(parsers[i].__str__())
        print "================================="

        self.debug = debug
        self.sustain = sustain
        self.parsers = parsers
        self.proxy_list = web_proxy_list
        for i in range(len(parsers)):
            self.proxy_list += parsers[i].parse_proxyList()
        self.current_proxy = self.randomize_proxy()

    def get_proxy_list(self):
        return self.proxy_list

    def generate_random_request_headers(self):
        headers = {
            "Connection": "close",  # another way to cover tracks
            "User-Agent": self.userAgent.get_random_user_agent()
        }  # select a random user agent
        return headers

    def randomize_proxy(self):
        rand_proxy = random.choice(self.proxy_list)
        while not rand_proxy:
            rand_proxy = random.choice(self.proxy_list)
        self.current_proxy = rand_proxy
        return rand_proxy

    def printd(self, msg):
        if self.debug:
            print msg

    #####
    # Proxy format:
    # http://<USERNAME>:<PASSWORD>@<IP-ADDR>:<PORT>
    #####
    def generate_proxied_request(self, url, method="GET", params={}, data={}, headers={}, req_timeout=30):
        try:
            random.shuffle(self.proxy_list)
            req_headers = dict(params.items() + self.generate_random_request_headers().items())

            if not self.sustain:
                self.randomize_proxy()

            self.printd("Using proxy: {0}".format(str(self.current_proxy)))
            request = requests.request(method, url, proxies={"http": self.current_proxy},
                                   headers=headers.update(req_headers), data=data, params=params, timeout=req_timeout)
            return request
        except ConnectionError:
            try:
                self.proxy_list.remove(self.current_proxy)
            except ValueError:
                pass
            self.printd("Proxy unreachable - Removed Straggling proxy: {0} PL Size = {1}".format(self.current_proxy, len(self.proxy_list)))
            self.randomize_proxy()
        except ReadTimeout:
            try:
                self.proxy_list.remove(self.current_proxy)
            except ValueError:
                pass
            self.printd("Read timed out - Removed Straggling proxy: {0} PL Size = {1}".format(self.current_proxy, len(self.proxy_list)))
            self.randomize_proxy()
        except ChunkedEncodingError:
            try:
                self.proxy_list.remove(self.current_proxy)
            except ValueError:
                pass
            self.printd("Wrong server chunked encoding - Removed Straggling proxy: {0} PL Size = {1}".format(self.current_proxy, len(self.proxy_list)))
            self.randomize_proxy()


if __name__ == '__main__':

    start = time.time()
    req_proxy = RequestProxy()
    print "Initialization took: {0} sec".format((time.time() - start))
    print "Size : ", len(req_proxy.get_proxy_list())
    print " ALL = ", req_proxy.get_proxy_list()

    test_url = 'http://icanhazip.com'

    while True:
        start = time.time()
        request = req_proxy.generate_proxied_request(test_url)
        print "Proxied Request Took: {0} sec => Status: {1}".format((time.time() - start), request.__str__())
        if request is not None:
            print "\t Response: ip={0}".format(request.text)
        print "Proxy List Size: ", len(req_proxy.get_proxy_list())

        print"-> Going to sleep.."
        time.sleep(10)
