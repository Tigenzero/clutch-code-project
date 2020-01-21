import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from .google_geocoder.google_geocoder import GoogleGeocoder


app = Flask(__name__)
app.config.from_object("geocoding.config.Config")
db = SQLAlchemy(app)

ADDRESS_ARG = 'address'

API_KEY = os.getenv("API_KEY")
GLOBAL_GOOGLE_GEOCODER = GoogleGeocoder(API_KEY)

# TODO: example code: replace with lat/long schema once determined
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(128), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def hello_world():
    return "Hello!"


@app.route('/search_address', methods=['GET'])
def geocode_address():
    if ADDRESS_ARG in request.args:
        address = request.args[ADDRESS_ARG]
    else:
        return "ERROR: Address not found. Please provide an address"

    lat_long = GLOBAL_GOOGLE_GEOCODER.get_address(address)
#     TODO: get the shape file state result from DB
    return jsonify(lat_long)