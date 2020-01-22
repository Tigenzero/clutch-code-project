import os
from flask.cli import FlaskGroup
from geocoding import app, db, PostGIS

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    PostGIS.create_borders_table()


@cli.command("seed_db")
def seed_db():
    PostGIS.seed_borders_table()


if __name__ == "__main__":
    cli()
