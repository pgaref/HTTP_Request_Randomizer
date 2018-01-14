from http_request_randomizer.web import db
from http_request_randomizer.web.common.models import ProxyData

db.create_all()

print("ProxyPad DB created.")
