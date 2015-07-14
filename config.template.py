import os
basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
TESTING = True

UPLOAD_FOLDER = '/path/to/the/uploads'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'cookies.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db', 'db_repository')

SECRET_KEY = 'change me !'
