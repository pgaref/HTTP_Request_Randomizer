"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""
from http_request_randomizer.requests.parsers.FreeProxyParser import FreeProxyParser
from http_request_randomizer.requests.parsers.ProxyForEuParser import ProxyForEuParser
from http_request_randomizer.requests.parsers.RebroWeeblyParser import RebroWeeblyParser
from http_request_randomizer.requests.parsers.SamairProxyParser import SamairProxyParser
from apscheduler.schedulers.background import BackgroundScheduler
from requests.exceptions import ReadTimeout
from sqlite3 import dbapi2 as sqlite3
from urlparse import urlparse
import logging
import time
import os

from http_request_randomizer.web.common import insert_proxy_db

logger = logging.getLogger(__name__)
logging.basicConfig()

__author__ = 'pgaref'


class ParsingScheduler:

    def __init__(self, database, timeout=5):
        parsers = list([])
        parsers.append(FreeProxyParser('http://free-proxy-list.net', timeout=timeout))
        parsers.append(ProxyForEuParser('http://proxyfor.eu/geo.php', 1.0, timeout=timeout))
        parsers.append(RebroWeeblyParser('http://rebro.weebly.com', timeout=timeout))
        parsers.append(SamairProxyParser('http://samair.ru/proxy/time-01.htm', timeout=timeout))
        self.parsers = parsers
        self.database = database
        self.scheduler = BackgroundScheduler()

    def tick(self):
        print('Tick! The time is: %s' % time.time())
        for parser in self.parsers:
            curr_proxy_list = []
            try:
                curr_proxy_list = parser.parse_proxyList()
            except ReadTimeout:
                print("Proxy Parser: '{}' TimedOut!".format(parser.url))
            finally:
                # Separate db connection per parser
                sqlite_db = sqlite3.connect(self.database)
                sqlite_db.row_factory = sqlite3.Row
                for current_proxy in curr_proxy_list:
                    parsed_proxy = urlparse(current_proxy)
                    insert_proxy_db(sqlite_db, proxy_ip=parsed_proxy.hostname, proxy_port=parsed_proxy.port,
                                    provider=parser.url)
                print("Inserted: {} proxies from: {}".format(len(curr_proxy_list), parser.url))

    def add_background_task(self, interval=60):
        self.scheduler.add_job(self.tick, 'interval', seconds=interval)

    def start_background_task(self):
        self.scheduler.start()

    def shutdown_background_task(self):
        self.scheduler.shutdown()


if __name__ == '__main__':
    ps = ParsingScheduler(database='/tmp/proxylist.db')
    ps.add_background_task(10)
    ps.start_background_task()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        ps.shutdown_background_task()
