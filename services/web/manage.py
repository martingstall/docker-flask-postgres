from flask.cli import FlaskGroup

from project import app
from project.models.shared import db
from project.models.users import User


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    #db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user = User(
        email="michael@mherman.org",
        first_name="Mike"
    )
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    cli()
