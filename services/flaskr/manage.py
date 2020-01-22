from flask.cli import FlaskGroup
from geocoding import app, db, PostGIS

cli = FlaskGroup(app)


# TODO: create and load data here
@cli.command("create_db")
def create_db():
    # db.drop_all()
    # db.create_all()
    # db.session.commit()
    PostGIS.create_db_connection()

@cli.command("seed_db")
def seed_db():
    pass
    # db.session.add(User(email="michael@mherman.org"))
    # db.session.commit()

if __name__ == "__main__":
    cli()
