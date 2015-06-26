from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from cookierun.database import db

from cookierun.controllers.main import main
from cookierun.controllers.cookie import cookies
from cookierun.controllers.route import routes
from cookierun.controllers.upload import upload

app = Flask(__name__)

db = SQLAlchemy(app)

app.register_blueprint(main)
app.register_blueprint(cookies, url_prefix='/cookies')
app.register_blueprint(routes, url_prefix='/routes')
app.register_blueprint(upload, url_prefix='/upload')

db.create_all()
