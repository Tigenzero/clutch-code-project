import googlemaps
from collections import deque


class GoogleGeocoder(object):
    def __init__(self, api_key):
        self.gmap = googlemaps.Client(key=api_key)
        self.queue = deque()

    def _get_geocoded_lat_long(self, address):
        geocode_object = self.gmap.geocode(address)
        return self._parse_geocode_object(geocode_object)

    def _parse_geocode_object(self, geocode_object):
        if len(geocode_object) > 0 and "geometry" in geocode_object[0] and "location" in geocode_object[0]["geometry"]:
            return geocode_object[0]["geometry"]["location"]
        elif len(geocode_object) == 0:
            raise LookupError(f"Address provided not found: {geocode_object}")
        elif len(geocode_object) > 0 and "geometry" in geocode_object[0]:
            raise KeyError(f"Address was found but location could not be determined. {geocode_object}")

    def get_lat_long_from_address(self, address):
        return self._get_geocoded_lat_long(address)
