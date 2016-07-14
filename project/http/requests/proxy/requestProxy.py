from project.http.requests.parsers.freeproxyParser import freeproxyParser
from project.http.requests.parsers.proxyforeuParser import proxyforeuParser
from project.http.requests.parsers.rebroweeblyParser import rebroweeblyParser
from project.http.requests.parsers.samairproxyParser import semairproxyParser

__author__ = 'pgaref'

import requests
from requests.exceptions import ConnectionError
import random
import os
import time
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout


class RequestProxy:
    agent_file = '../data/user_agents.txt'

    def __init__(self, web_proxy_list=[]):
        self.useragents = self.load_user_agents(RequestProxy.agent_file)
        #####
        # Each of the classes below implements a specific URL Parser
        # http://<USERNAME>:<PASSWORD>@<IP-ADDR>:<PORT>
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

        self.parsers = parsers
        self.proxy_list = web_proxy_list
        for i in range(len(parsers)):
            self.proxy_list += parsers[i].parse_proxyList()


    def get_proxy_list(self):
        return self.proxy_list

    def load_user_agents(self, useragentsfile):
        """
        useragentfile : string
            path to text file of user agents, one per line
        """
        useragents = []
        with open(useragentsfile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    useragents.append(ua.strip()[1:-1-1])
        random.shuffle(useragents)
        return useragents

    def get_random_user_agent(self):
        """
        useragents : string array of different user agents
        :param useragents:
        :return random agent:
        """
        user_agent = random.choice(self.useragents)
        return user_agent

    def generate_random_request_headers(self):
        headers = {
            "Connection": "close",  # another way to cover tracks
            "User-Agent": self.get_random_user_agent()
        }  # select a random user agent
        return headers

    #####
    # Proxy format:
    # http://<USERNAME>:<PASSWORD>@<IP-ADDR>:<PORT>
    #####
    def generate_proxied_request(self, url, params={}, req_timeout=30):
        random.shuffle(self.proxy_list)
        req_headers = dict(params.items() + self.generate_random_request_headers().items())

        request = None
        try:
            rand_proxy = random.choice(self.proxy_list)
            print "Using proxy: " + str(rand_proxy)
            request = requests.get(test_url, proxies={"http": rand_proxy},
                                   headers=req_headers, timeout=req_timeout)
        except ConnectionError:
            self.proxy_list.remove(rand_proxy)
            print "Proxy unreachable - Removed Straggling proxy :", rand_proxy, " PL Size = ",len(self.proxy_list)
            pass
        except ReadTimeout:
            self.proxy_list.remove(rand_proxy)
            print "Read timed out - Removed Straggling proxy :", rand_proxy, " PL Size = ", len(self.proxy_list)
            pass
        return request

if __name__ == '__main__':

    start = time.time()
    req_proxy = RequestProxy()
    print "Initialization took: ", (time.time()-start)
    print "Size : ", len(req_proxy.get_proxy_list())
    print " ALL = ", req_proxy.get_proxy_list()

    test_url = 'http://localhost:8888'

    while True:
        start = time.time()
        request = req_proxy.generate_proxied_request(test_url)
        print "Proxied Request Took: ", (time.time()-start), " => Status: ", request.__str__()
        print "Proxy List Size: ", len(req_proxy.get_proxy_list())

        print"-> Going to sleep.."
        time.sleep(10)
