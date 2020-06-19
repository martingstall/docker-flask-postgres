from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from project.blueprints import framework_template

from project.models.framework_template import FrameworkTemplateSchema, PhaseSchema
from project.models.framework_template import FrameworkTemplateParams


spec_v2 = APISpec(
    title="Omniscope 2.0",
    version="1.0.0",
    openapi_version="3.0.3",
    info=dict(description="TBD"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

#spec_v2.components.schema("FrameworkTemplate", schema=FrameworkTemplateSchema)
#spec_v2.components.schema("FrameworkTemplateParams", schema=FrameworkTemplateParams)
