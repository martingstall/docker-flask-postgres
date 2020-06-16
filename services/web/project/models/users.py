from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from project.database import Base


@dataclass
class User(Base):
    id: int
    email: str
    first_name: str
    active: bool

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True, nullable=False)
    first_name = Column(String(128), nullable=False)
    active = Column(Boolean(), default=True, nullable=False)

    def __str__(self):
        return "%s" % self.email
