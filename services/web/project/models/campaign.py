from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from project.models.shared import db


@dataclass
class Step(db.Model):
    id: int
    name: str
    phase_id: int

    __tablename__ = "steps"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    phase_id = db.Column(db.Integer, ForeignKey('phases.id'))

    phases = relationship("Phase", back_populates="steps")

    def __str__(self):
        return "%s" % self.name


@dataclass
class Phase(db.Model):
    id: int
    name: str
    campaign_id: int
    steps: Step

    __tablename__ = "phases"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    campaign_id = db.Column(db.Integer, ForeignKey('campaigns.id'))

    steps = relationship("Step", back_populates="phases")
    campaigns = relationship("Campaign", back_populates="phases")

    def __str__(self):
        return "%s" % self.name


@dataclass
class Campaign(db.Model):
    id: int
    name: str
    active: bool
    phases: Phase

    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    phases = relationship("Phase", back_populates="campaigns")
