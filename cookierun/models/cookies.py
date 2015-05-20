from cookierun.database import db


class Cookie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    calories = db.Column(db.Float)
    brand = db.Column(db.String(255))
    website = db.Column(db.Text)

    def __init__(self, name, calories, brand, website):
        self.name = name
        self.calories = calories
        self.brand = brand
        self.website = website

    def __repr__(self):
        return '<Cookie %d>' % self.id
