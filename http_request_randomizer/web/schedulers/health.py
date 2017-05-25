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


class HealthScheduler:

    def __init__(self, proxies, timeout=5):
        self.all_proxies = proxies
        self.scheduler = BackgroundScheduler()

    def tick(self):
        print('Tick! The time is: %s' % time.time())
        # TODO: Check Proxy health and Anonymity level!

    def add_background_task(self, interval=60):
        self.scheduler.add_job(self.tick, 'interval', seconds=interval)

    # TODO: Connect task with APP
    def start_background_task(self):
        self.scheduler.start()

    def shutdown_background_task(self):
        self.scheduler.shutdown()


