import json
from pprint import pprint

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from project.models.framework_template import FrameworkTemplateSchema, PhaseSchema


spec = APISpec(
    title="Omniscope 2.0",
    version="1.0.0",
    openapi_version="3.0.3",
    info=dict(description="TBD"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
spec.components.schema("FrameworkTemplate", schema=FrameworkTemplateSchema)

#print(json.dumps(spec.to_dict()))
print(spec.to_yaml())
