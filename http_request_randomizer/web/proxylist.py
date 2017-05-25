# -*- coding: utf-8 -*-
"""
    ProxyList
    ~~~~~~~~

    A Free-Proxy Web application written with Flask and sqlite3.

    :copyright: (c) 2017 by Panagiotis Garefalaksi.
    :license: MIT, see LICENSE for more details.
"""
import json
from datetime import datetime
from sqlite3 import dbapi2 as sqlite3

from flask import Flask, url_for, redirect, render_template, flash, _app_ctx_stack
from flask import Response

from http_request_randomizer.web.common import query_db, query_db_jsonified
from http_request_randomizer.web.schedulers.parsing import ParsingScheduler

# configuration
DATABASE = '/tmp/proxylist.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'


# create our little application :)
app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
app.config.from_envvar('PROXYLIST_SETTINGS', silent=True)



@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.route('/')
def index():
    """Shows top-Proxies to a human user by redirecting to the public index.
    If we find a robot we display a different page
    """
    return redirect(url_for('public_index'))


@app.route('/public_index')
def public_index():
    """Displays the latest top Proxies"""
    return render_template('public_index.html', messages=query_db(get_db(), '''
        select message.*, user.* from message, user
        where message.author_id = user.user_id
        order by message.pub_date desc limit ?''', [PER_PAGE]),
                           proxies=query_db(get_db(), '''
        select proxy.* from proxy
        order by proxy.add_date desc limit ?''', [PER_PAGE])
                           )


@app.route('/top<number>')
def top_proxies(number):
    """Returns the latest top Proxies as json representation"""
    if 0 < int(number) <= 100:
        number_proxies = query_db_jsonified(get_db(), '''
        select proxy.ip, proxy.port from proxy
        order by proxy.add_date desc limit ?''', [number])
        return Response(json.dumps(number_proxies), mimetype='application/json')
    else:
        flash("Use REST API wisely!!")
        return redirect(url_for('public_index'))


def format_datetime(timestamp):
    """Format a timestamp for display."""
    if timestamp is None:
        return "Never"
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime


if __name__ == '__main__':
    bg_parser = ParsingScheduler(DATABASE)
    bg_parser.add_background_task(60)
    bg_parser.start_background_task()
    app.run()