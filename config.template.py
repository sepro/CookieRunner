import os
basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
TESTING = True

ADMIN_PASSWORD = 'admin'

UPLOAD_FOLDER = os.path.join(basedir, 'tmp')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'cookies.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db', 'db_repository')

SECRET_KEY = 'change me !'
