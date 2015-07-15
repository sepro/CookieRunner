#!/usr/bin/env python3
"""

Script to create the initial database and migration information

"""
from migrate.versioning import api

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from config import UPLOAD_FOLDER
from config import ADMIN_PASSWORD

from cookierun import app, db

from cookierun.models.users import User
from cookierun.models.cookies import Cookie

import os.path

db.create_all(app=app)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print("\nThe upload folder has been created")

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

# If there are no users in the database create an admin account
if len(User.query.all()) == 0:
    db.session.add(User("admin", ADMIN_PASSWORD, "admin@website.com", is_admin=True))
    db.session.commit()

    print("\nAn admin account has been created. Username=\'admin\' and password=\'" + ADMIN_PASSWORD + "\'")
    print("IMPORTANT: Change the password for this account")

# If there are no cookies in the database add a default list
if len(Cookie.query.all()) == 0:
    db.session.add(Cookie('Oreo - Original', 53.0, 'Oreo', 'www.oreo.com'))
    db.session.add(Cookie('Oreo - Chocolate Cream', 51.0, 'Oreo', 'www.oreo.com'))
    db.session.add(Cookie('Oreo - White Choc', 105.0, 'Oreo', 'www.oreo.com'))
    db.session.add(Cookie('Oreo - Milk Choc', 105.0, 'Oreo', 'www.oreo.com'))
    db.session.add(Cookie('Pim''s Orange', 50.0, 'LU', 'http://www.lubiscuits.com/'))
    db.session.add(Cookie('Pim''s Raspberry', 50.0, 'LU', 'http://www.lubiscuits.com/'))
    db.session.add(Cookie('Dinosaurus Chocolate', 95.0, 'Lotus', 'http://www.lotusbakeries.com/'))
    db.session.add(Cookie('Dinosaurus Milk Chocolate', 94.0, 'Lotus', 'http://www.lotusbakeries.com/'))
    db.session.add(Cookie('Dinosaurus Grains', 71.0, 'Lotus', 'http://www.lotusbakeries.com/'))
    db.session.commit()

    print("\nA default list of cookies has been added to the database.")
