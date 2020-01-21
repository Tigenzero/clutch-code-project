import googlemaps
from collections import deque


class GoogleGeocoder(object):
    def __init__(self, api_key):
        self.gmap = googlemaps.Client(key=api_key)
        self.queue = deque()

    def _get_address_lat_long(self, address):
        geocode_object = self.gmap.geocode(address)
        return self._parse_geocode_object(geocode_object)

    def _parse_geocode_object(self, geocode_object):
        return geocode_object[0]["geometry"]["location"]

    def get_address(self, address, debug_delay=False):
        # TODO: implement queue of threads to handle the IO
        return self._get_address_lat_long(address)
