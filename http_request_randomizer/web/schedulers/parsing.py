"""
Use a background scheduler to schedule a job that parses periodically the available providers.
"""
import logging
import os
import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from requests.exceptions import ReadTimeout

from http_request_randomizer.requests.parsers.FreeProxyParser import FreeProxyParser
from http_request_randomizer.requests.parsers.ProxyForEuParser import ProxyForEuParser
from http_request_randomizer.requests.parsers.RebroWeeblyParser import RebroWeeblyParser
from http_request_randomizer.requests.parsers.SamairProxyParser import SamairProxyParser
from http_request_randomizer.web.common.queries import db_store_proxy_object

logger = logging.getLogger(__name__)
logging.basicConfig()

__author__ = 'pgaref'


class ParsingScheduler:

    def __init__(self, timeout=5):
        parsers = list([])
        parsers.append(RebroWeeblyParser('ReBro', 'http://rebro.weebly.com', timeout=timeout))
        parsers.append(SamairProxyParser('Samair', 'https://premproxy.com', timeout=timeout))
        parsers.append(FreeProxyParser('FreeProxy', 'http://free-proxy-list.net', timeout=timeout))
        parsers.append(ProxyForEuParser('ProxyForEU', 'http://proxyfor.eu/geo.php',
                                        bandwidth=10, timeout=timeout))
        self.parsers = parsers
        self.scheduler = BackgroundScheduler()

    def tick(self):
        print('Parser cycle: {0}'.format(datetime.utcnow()))
        for parser in self.parsers:
            curr_proxy_list = []
            try:
                curr_proxy_list = parser.parse_proxyList()
            except ReadTimeout:
                print("Proxy Parser: '{}' TimedOut!".format(parser.url))
            finally:
                for current_proxy in curr_proxy_list:
                    db_store_proxy_object(current_proxy)
                print("Inserted: {} proxies from: {}".format(len(curr_proxy_list), parser.url))

    def add_background_task(self, interval=60):
        self.scheduler.add_job(self.tick, 'interval', seconds=interval)

    def start_background_task(self):
        self.scheduler.start()

    def shutdown_background_task(self):
        self.scheduler.shutdown()


if __name__ == '__main__':
    ps = ParsingScheduler()
    ps.add_background_task(60)
    ps.start_background_task()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        ps.shutdown_background_task()
