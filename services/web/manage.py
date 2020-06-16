from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask.cli import FlaskGroup

from project import app
from project.database import Session, engine

from project.models.users import User

cli = FlaskGroup(app)
db = Session()
migrate = Migrate(app, db)

manager = Manager(app)
"""
python manage.py db migrate
python manage.py db upgrade
"""
manager.add_command('db', MigrateCommand)


@cli.command("create_db")
def create_db():
    #db.drop_all()
    #db.create_all()
    #db.session.commit()
    pass


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
    manager.run()
