from flask.cli import FlaskGroup

from project import app
from project.database import Base, Session, engine

from sqlalchemy import *
from project.models.framework_template import FrameworkTemplate, Phase, Step

cli = FlaskGroup(app)
db = Session()


@cli.command("create_db")
def create_db():
    Base.metadata.create_all(engine)

    print("Initialized the db")


@cli.command("seed_db")
def seed_db():
    """
    user = User(
        email="michael@mherman.org",
        first_name="Mike"
    )
    db.add(user)
    db.commit()
    """
    pass


if __name__ == "__main__":
    cli()
    manager.run()
