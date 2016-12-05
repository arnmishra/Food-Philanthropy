""" App to host Google Maps of Location and Nearby Pantries.

Week 0 Requirements:
1. App Renders correctly with current locations
2. Nearby Pantries are displayed
3. Postmates quotes are returned correctly

Week 1 Requirements:
1. Uber API Interactions
2. Asynchronous submission form linked with Uber + Postmates
3. Develop Google Maps Routing

Week 2 Requirements:
1. SQL Alchemy integrations for authentication
2. SQL Models for Routing
3. Registration
4. Login/Logout

Week 3 Requirements:
1. Cumulative Stats
2. Past Order Paths
3. Auto-Fill User Info
4. Routes Model
"""

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
