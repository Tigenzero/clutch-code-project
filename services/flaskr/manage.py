from flask.cli import FlaskGroup
from geocoding import app, global_PostGIS

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    global_PostGIS.create_borders_table()


@cli.command("seed_db")
def seed_db():
    global_PostGIS.seed_borders_table()


if __name__ == "__main__":
    cli()
