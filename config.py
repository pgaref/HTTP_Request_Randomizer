# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://proxypad:caf39f756871906f@proxypad-rds.cmnnnyzv5ado.us-west-2.rds.amazonaws.com:3306/proxypaddb'

# Uncomment the line below if you want to work with a local DB
# SQLALCHEMY_DATABASE_URI = 'sqlite:///proxypad-dev.db'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 3600
PROXIES_PER_PAGE = 20

WTF_CSRF_ENABLED = True
SECRET_KEY = 'fcee20bce87dfe5a989bca6f57078c32168ff6775f39830d'
DEBUG = True
