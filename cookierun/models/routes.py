from cookierun.database import db
from sqlalchemy.sql import null


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_key = db.Column(db.Text)
    distance = db.Column(db.Float)
    calories = db.Column(db.Float)
    speed = db.Column(db.Float)
    duration = db.Column(db.Float)
    gpx = db.Column(db.Text)
    user_id = db.Column(db.Integer)

    def __init__(self, file_key, distance, calories, speed, duration, gpx, user_id=null):
        self.file_key = file_key
        self.distance = distance
        self.calories = calories
        self.speed = speed
        self.duration = duration
        self.gpx = gpx
        self.user_id = user_id

    def __repr__(self):
        return '<Route %d>' % self.id
