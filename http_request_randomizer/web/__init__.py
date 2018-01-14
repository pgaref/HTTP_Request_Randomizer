from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = 'pgaref'

application = Flask(__name__, static_folder='static')
application.config.from_object('config')
db = SQLAlchemy(application)