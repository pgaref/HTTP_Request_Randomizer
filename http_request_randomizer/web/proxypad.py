"""
    ProxyList
    ~~~~~~~~

    www.proxypad.com web application written with Flask and SQLAlchemy.

    :copyright: (c) 2018 by Panagiotis Garefalakis.
    :license: MIT, see LICENSE for more details.
"""
import json
from datetime import datetime

from flask import url_for, redirect, render_template, Response, flash

from http_request_randomizer.requests.proxy.ProxyObject import AnonymityLevel
from http_request_randomizer.web import db, application

from http_request_randomizer.web.common.models import ProxyData
from http_request_randomizer.web.common.queries import db_get_proxy_results
from http_request_randomizer.web.schedulers.parsing import ParsingScheduler

import logging
file_handler = logging.FileHandler('proxypad.log')
application.logger.addHandler(file_handler)
application.logger.setLevel(logging.INFO)

__author__ = 'pgaref'

# Global Conf
PER_PAGE = 30

# Elastic Beanstalk initalization
# application = Flask(__name__, static_folder='static')
# application.config.from_object(__name__)
# application.config.from_envvar('PROXYPAD_SETTINGS', silent=False)


@application.teardown_appcontext
def shutdown_session(exception=None):
    """Closes the database again at the end of the request."""
    db.session.remove()

@application.route('/',  methods=['GET'])
def index():
    """Shows top-Proxies to a human user by redirecting to the public index.
        If we find a robot can display a different page
    """
    return redirect(url_for('public_index'))


@application.route('/index',  methods=['GET'])
def public_index():
    """Displays the latest top Proxies"""
    try:
        query_db = ProxyData.query.order_by(ProxyData.check_date.desc()).limit(PER_PAGE)
        db.session.close()
    except:
        db.session.rollback()
    return render_template('public_index.html',proxies=query_db)


@application.route('/top<number>')
def top_proxies(number):
    """Returns the latest top Proxies as json representation"""
    if 0 < int(number) <= 100:
        filtered_proxies = db_get_proxy_results(number)
        return Response(json.dumps(filtered_proxies), mimetype='application/json')
    else:
        flash("ProxyPad API limited to top100 proxies")
        return redirect(url_for('public_index'))


def format_datetime(proxy_datetime):
    """Format a datetime for display."""
    if proxy_datetime is None:
        return "Never"
    return proxy_datetime.strftime('%Y-%m-%d %H:%M')


def anonymityformat(anonymity_lvl):
    """Format a anonymity level for display."""
    return AnonymityLevel.get(anonymity_lvl).name


# add some filters to jinja
application.jinja_env.filters['datetimeformat'] = format_datetime
application.jinja_env.filters['anonymityformat'] = anonymityformat


if __name__ == '__main__':
    bg_parser = ParsingScheduler()
    bg_parser.add_background_task(30*60)
    bg_parser.start_background_task()
    application.run(host='0.0.0.0')