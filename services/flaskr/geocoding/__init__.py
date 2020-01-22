import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from .google_geocoder.google_geocoder import GoogleGeocoder
from .postgis.postgis import PostGIS


app = Flask(__name__)
app.config.from_object("geocoding.config.Config")
db = SQLAlchemy(app)

ADDRESS_ARG = 'address'

API_KEY = os.getenv("API_KEY")
global_google_geocoder = GoogleGeocoder(API_KEY)
PostGIS = PostGIS()


@app.route("/")
def hello_world():
    return "Hello!"


@app.route('/search_address', methods=['GET'])
def geocode_address():
    if ADDRESS_ARG in request.args:
        address = request.args[ADDRESS_ARG]
    else:
        return "ERROR: Address not found. Please provide an address"

    # lat_long_dict = GLOBAL_GOOGLE_GEOCODER.get_address(address)
    lat_long_dict = {'lat': 30.2587478, 'lng': -97.6716534}
    # print(lat_long_dict)
    result = PostGIS.get_state_from_lat_long(lat_long_dict)
    return jsonify({"state": result})
