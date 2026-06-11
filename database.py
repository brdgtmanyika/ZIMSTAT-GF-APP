from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EAData(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    geocode = db.Column(db.String(20), unique=True)

    ea_name = db.Column(db.String(100))

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    estimated_population = db.Column(db.Integer)

    households = db.Column(db.Integer)

    image_path = db.Column(db.String(200))

    boundary_file = db.Column(db.String(200))
