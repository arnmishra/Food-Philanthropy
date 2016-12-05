""" App to host Google Maps of Location and Nearby Pantries."""

from flask import Flask
from flask_googlemaps import GoogleMaps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from project import models

db.drop_all()
db.create_all()

GOOGLEMAPS_KEY = "AIzaSyDxWR2xwaBEyhzsD6aSZYH_alyOYZISJ1A"

app.config['GOOGLEMAPS_KEY'] = GOOGLEMAPS_KEY
GoogleMaps(app)

from project import views
