import os.path
import psycopg2
import osgeo.ogr


class PostGIS(object):
    def __init__(self, db_uri="", radius=5):
        self.connection = None
        if len(db_uri) == 0:
            self.db_uri = os.getenv("DATABASE_URL")
        else:
            self.db_uri = db_uri
        self.radius = radius

    def create_db_connection(self):
        self.connection = psycopg2.connect(self.db_uri)

    def get_state_from_lat_long(self, lat_long_dict):
        # TODO: Implement Connection Pooling!
        # if self.connection and self.connection.closed:
        #     self.create_db_connection()
        self.connection = psycopg2.connect(self.db_uri)
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM borders WHERE ST_DWithin("
                       "ST_MakePoint(%s, %s), outline, %s)",
                       (lat_long_dict["lng"], lat_long_dict["lat"], self.radius))
        for row in cursor:
            if isinstance(row, tuple):
                return row[0]
        return None
