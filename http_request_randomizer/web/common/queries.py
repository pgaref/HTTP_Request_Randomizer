from datetime import datetime

from http_request_randomizer.web import db
from http_request_randomizer.web.common.models import ProxyData

__author__ = 'pgaref'


def db_store_proxy_object(proxy_object):
    try:
        proxy_data = ProxyData(proxy_object=proxy_object, pub_date=datetime.utcnow())
        db.session.add(proxy_data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def db_get_proxy_results(num_return):
    try:
        proxy_data = ProxyData.query.order_by(ProxyData.check_date).limit(num_return).all()
        proxy_serial = dict((i + 1, proxy.get_address()) for i, proxy in enumerate(proxy_data))
        db.session.close()
    except Exception as e:
        print(e)
        db.session.rollback()
    return proxy_serial
