"""
Use a background scheduler to schedule a job that executes periodically and checks proxy health.
"""
import logging
import os
import time
import urllib2
from datetime import datetime
from dateutil import rrule

from apscheduler.schedulers.background import BackgroundScheduler

from config import PROXIES_PER_PAGE
from http_request_randomizer.requests.useragent.userAgent import UserAgentManager
from http_request_randomizer.web import db, application
from http_request_randomizer.web.common.models import ProxyData

logger = logging.getLogger(__name__)
logging.basicConfig()

__author__ = 'pgaref'


class HealthScheduler:

    def __init__(self, timeout=2):
        self.timeout = timeout
        self.userAgent = UserAgentManager()
        self.scheduler = BackgroundScheduler()
        self.proxy_iterator = None

    def tick(self):
        application.logger.info('Health cycle: {0}'.format(datetime.utcnow()))
        # Check Proxy health
        proxies = self.get_next_proxy_batch()
        try:
            # TODO: Validate anonymity level
            for proxy in proxies:
                if self.is_healthy_proxy(proxy.get_address()):
                    proxy.check_date = datetime.utcnow()
                # elif self.get_weeks_between(proxy.check_date) >= 1:
                #     db.session.delete(proxy)
            db.session.commit()
        except Exception as e:
            raise(e)
            db.session.rollback()

    def add_background_task(self, interval=60):
        self.scheduler.add_job(self.tick, 'interval', seconds=interval)

    def start_background_task(self):
        self.scheduler.start()

    def shutdown_background_task(self):
        self.scheduler.shutdown()

    @staticmethod
    def get_weeks_between(start_date, end_date=datetime.utcnow()):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()

    def get_next_proxy_batch(self):
        if self.proxy_iterator is None or not self.proxy_iterator.has_next:
            next_page = 1
        elif self.proxy_iterator.has_next:
            next_page = self.proxy_iterator.next_num
        return ProxyData.query.order_by(ProxyData.check_date.asc()) \
            .paginate(next_page, PROXIES_PER_PAGE, False).items

    def is_healthy_proxy(self, proxy_address):
        try:
            proxy_handler = urllib2.ProxyHandler({'http': proxy_address})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [
                ("Connection", "close"),
                ('User-agent', self.userAgent.get_random_user_agent())
            ]
            urllib2.install_opener(opener)
            req = urllib2.Request('http://www.example.com')
            sock = urllib2.urlopen(req, timeout=self.timeout)
        except urllib2.HTTPError, e:
            application.logger.warn("PROXY {} ERROR {}".format(proxy_address, e.code))
            return False
        except Exception, detail:
            application.logger.warn("PROXY {} ERROR {}".format(proxy_address, detail))
            return False
        application.logger.info("PROXY {} OK".format(proxy_address))
        return True


if __name__ == '__main__':
    hs = HealthScheduler()
    hs.add_background_task(60)
    hs.start_background_task()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        hs.shutdown_background_task()
