from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from cookierun.controllers.main import main
from cookierun.controllers.cookie import cookie

app = Flask(__name__)

db = SQLAlchemy(app)

app.register_blueprint(main)
app.register_blueprint(cookie)

db.create_all()
