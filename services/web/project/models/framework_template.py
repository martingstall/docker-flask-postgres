from dataclasses import dataclass

from marshmallow import Schema, fields, post_load

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, SmallInteger
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from project.database import Base


class StepSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)

    @post_load
    def make_framework_template(self, data, **kwargs):
        return Step(**data)


class PhaseSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    steps = fields.List(fields.Nested(StepSchema))

    @post_load
    def make_framework_template(self, data, **kwargs):
        return Phase(**data)


class FrameworkTemplateSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    diagram = fields.Str(required=True)
    active = fields.Bool()
    phases = fields.List(fields.Nested(PhaseSchema))

    @post_load
    def make_framework_template(self, data, **kwargs):
        return FrameworkTemplate(**data)


@dataclass
class Step(Base):
    id: int
    name: str
    phase_id: int

    __tablename__ = "steps"

    id = Column(Integer, primary_key=True)
    phase_id = Column(Integer, ForeignKey('phases.id'))
    name = Column(String(128), nullable=False)
    description = Column(Text)
    display_order = Column(SmallInteger)
    data_entry_form = Column(JSON)

    phases = relationship("Phase", back_populates="steps")

    def __str__(self):
        return "%s" % self.name


@dataclass
class Phase(Base):
    id: int
    name: str
    framework_template_id: int
    steps: Step

    __tablename__ = "phases"

    id = Column(Integer, primary_key=True)
    framework_template_id = Column(Integer, ForeignKey('framework_templates.id'))
    name = Column(String(128), nullable=False)
    description = Column(Text)
    display_order = Column(SmallInteger)
    css_position = Column(String(128), nullable=True)

    steps = relationship("Step", back_populates="phases")
    framework_templates = relationship("FrameworkTemplate", back_populates="phases")

    def __str__(self):
        return "%s" % self.name


@dataclass
class FrameworkTemplate(Base):
    id: int
    name: str
    active: bool
    phases: Phase

    __tablename__ = "framework_templates"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    diagram = Column(String(255), nullable=True)
    active = Column(Boolean(), default=True, nullable=False)

    phases = relationship("Phase", back_populates="framework_templates")

    def __str__(self):
        return "%s" % self.name
