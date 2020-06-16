from dataclasses import dataclass
from project.models.shared import db


@dataclass
class User(db.Model):
    id: int
    email: str
    first_name: str
    active: bool
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __str__(self):
        return "%s" % self.email

    @property
    def serialized(self):
        """

        :return:
        :rtype:
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
