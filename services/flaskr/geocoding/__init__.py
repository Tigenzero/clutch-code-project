import os
from flask import Flask, jsonify, request
from .google_geocoder.google_geocoder import GoogleGeocoder
from .postgis.postgis import PostGIS


app = Flask(__name__)

ADDRESS_ARG = 'address'

API_KEY = os.getenv("API_KEY")
global_google_geocoder = GoogleGeocoder(API_KEY)
global_PostGIS = PostGIS()


@app.route("/")
def hello_world():
    return "Hello! Please proceed to 0.0.0.0/search_address?search_address='your address!'"


@app.route('/search_address', methods=['GET'])
def geocode_address():
    if ADDRESS_ARG in request.args:
        address = request.args[ADDRESS_ARG]
    else:
        return jsonify({"ERROR": "Address not found. Please provide an address"})

    lat_long_dict = global_google_geocoder.get_address(address)
    result = global_PostGIS.get_state_from_lat_long(lat_long_dict)
    return jsonify({"state": result})
