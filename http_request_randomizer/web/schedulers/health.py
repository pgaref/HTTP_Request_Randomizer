"""
Use a background scheduler to schedule a job that executes periodically and checks proxy health.
"""
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)
logging.basicConfig()

__author__ = 'pgaref'


class HealthScheduler:

    def __init__(self, proxies, timeout=5):
        self.all_proxies = proxies
        self.scheduler = BackgroundScheduler()

    def tick(self):
        print('Health cycle: {0}'.format(datetime.utcnow()))
        # TODO: Check Proxy health and Anonymity level!

    def add_background_task(self, interval=60):
        self.scheduler.add_job(self.tick, 'interval', seconds=interval)

    # TODO: Connect task with APP
    def start_background_task(self):
        self.scheduler.start()

    def shutdown_background_task(self):
        self.scheduler.shutdown()
