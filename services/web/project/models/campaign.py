from dataclasses import dataclass

from marshmallow import Schema, fields, pre_load

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from project.database import Base


class StepSchema(Schema):
    id = fields.Int()
    name = fields.Str()


@dataclass
class Step(Base):
    id: int
    name: str
    phase_id: int

    __tablename__ = "steps"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    phase_id = Column(Integer, ForeignKey('phases.id'))

    phases = relationship("Phase", back_populates="steps")

    def __str__(self):
        return "%s" % self.name


class PhaseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    steps = fields.List(fields.Nested(StepSchema), required=True)


@dataclass
class Phase(Base):
    id: int
    name: str
    campaign_id: int
    steps: Step

    __tablename__ = "phases"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))

    steps = relationship("Step", back_populates="phases")
    campaigns = relationship("Campaign", back_populates="phases")

    def __str__(self):
        return "%s" % self.name


class CampaignSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    active = fields.Bool()
    phases = fields.List(
        fields.Nested(
            PhaseSchema(only=("name","steps",))
        ), required=True
    )


@dataclass
class Campaign(Base):
    id: int
    name: str
    active: bool
    phases: Phase

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    active = Column(Boolean(), default=True, nullable=False)

    phases = relationship("Phase", back_populates="campaigns")

    def __str__(self):
        return "%s" % self.name
