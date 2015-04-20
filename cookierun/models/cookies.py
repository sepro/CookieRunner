from cookierunner import db

class Cookie(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    calories = db.Column(db.Float)

    def __init__(self, name, calories):
        self.name = name
        self.calories = calories

    def __repr__(self):
        return '<Cookie %d>' % self.id

