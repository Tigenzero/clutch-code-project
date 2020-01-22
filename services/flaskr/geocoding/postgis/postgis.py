import os.path
import psycopg2
from psycopg2 import pool
from osgeo import ogr
import logging


class PostGIS(object):
    def __init__(self, db_uri="", radius=5):
        self.__connection = None
        if len(db_uri) == 0:
            self.db_uri = os.getenv("DATABASE_URL")
        else:
            self.db_uri = db_uri
        self.radius = radius

    def _create_db_connection(self):
        self.__connection = psycopg2.pool.SimpleConnectionPool(5, 20, self.db_uri)
        if not self.__connection:
            raise ConnectionError("Connection to PostGreSQL DB failed.")

    def _get_db_connection(self):
        if not self.__connection:
            self._create_db_connection()
        return self.__connection.getconn()

    def _return_db_connection(self, connection):
        self.__connection.putconn(connection)

    def create_borders_table(self):
        logging.info("Creating Table")
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS borders")
        cursor.execute("CREATE TABLE borders (id SERIAL PRIMARY KEY,"
                       "name VARCHAR NOT NULL,"
                       "outline GEOGRAPHY)")
        cursor.execute("CREATE INDEX border_index ON borders " +
                       "USING GIST(outline)")
        connection.commit()
        self._return_db_connection(connection)

    def get_shapefile(self, shapefile_path=""):
        if len(shapefile_path) == 0:
            shapefile_path = os.getenv("SHAPEFILE_PATH")
        if not os.path.exists(shapefile_path):
            raise FileNotFoundError(f"File path not found: {shapefile_path}")
        return ogr.Open(shapefile_path)

    def get_feature_fields(self, feature):
        name = feature.GetField("NAME")
        geometry = feature.GetGeometryRef()
        wkt = geometry.ExportToWkt()
        return name, wkt

    def seed_borders_table(self):
        logging.info("Seeding Table")
        connection = self._get_db_connection()
        cursor = connection.cursor()
        shapefile = self.get_shapefile()
        layer = shapefile.GetLayer(0)
        print()
        for i in range(layer.GetFeatureCount()):
            fields = self.get_feature_fields(layer.GetFeature(i))
            cursor.execute("INSERT INTO borders (name, outline) "
                           "VALUES (%s, ST_GeogFromText(%s))", fields)
        connection.commit()
        self._return_db_connection(connection)

    def get_state_from_lat_long(self, lat_long_dict):
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM borders WHERE ST_DWithin("
                       "ST_MakePoint(%s, %s), outline, %s)",
                       (lat_long_dict["lng"], lat_long_dict["lat"], self.radius))
        result = None
        for row in cursor:
            result = row[0]
        cursor.close()
        self._return_db_connection(connection)
        return result
