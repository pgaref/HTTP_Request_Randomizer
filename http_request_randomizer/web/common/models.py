from datetime import datetime

from http_request_randomizer.web import db

__author__ = 'pgaref'


class ProxyData(db.Model):
    __tablename__ = 'proxy_data'
    ip = db.Column(db.String(64), nullable=False, primary_key=True)
    port = db.Column(db.Integer, nullable=False, primary_key=True)
    provider = db.Column(db.String(32), unique=False, nullable=False)
    anonymity_level = db.Column(db.Integer)
    country = db.Column(db.String(32))
    protocols = db.Column(db.String(64))
    tunnel = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime, nullable=False)
    check_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, proxy_object, pub_date, check_date=None):
        self.ip = proxy_object.ip
        self.port = proxy_object.port
        self.provider = proxy_object.source
        self.anonymity_level = proxy_object.anonymity_level.value
        self.country = proxy_object.country
        self.protocols = str(proxy_object.protocols)
        self.tunnel = proxy_object.tunnel
        self.pub_date = pub_date
        self.check_date = check_date

    def __repr__(self):
        return '<ProxyData {0}:{1}>'.format(self.ip, self.port, self.provider, self.pub_date)

    def get_address(self):
        return "{0}:{1}".format(self.ip, self.port)
