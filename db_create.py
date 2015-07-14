from cookierun import app
from cookierun.models.runs import db


db.create_all(app=app)
