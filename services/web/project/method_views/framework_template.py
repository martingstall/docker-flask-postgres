from marshmallow import ValidationError

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request
)
from flask.views import MethodView

from project.database import Session
from project.models.framework_template import FrameworkTemplate as FrameworkTemplateModel
from project.models.framework_template import FrameworkTemplateSchema, FrameworkTemplateParams
from project.resources import helpers

db = Session()


class FrameworkTemplate(MethodView):

    def get(self, framework_template_id):
        """Framework Template view
        ---
        description: Get a Framework Template
        parameters:
        - in: path
          name: framework_template_id
          required: true
          schema:
            type: integer
          description: The framework template ID
        responses:
          200:
            content:
              application/json:
                schema: FrameworkTemplateSchema
        """
        args = request.args
        data = db.query(FrameworkTemplateModel).get(framework_template_id)
        only_fields = helpers.get_only_fields(args)

        if only_fields:
            schema = FrameworkTemplateSchema(only=(only_fields))
        else:
            schema = FrameworkTemplateSchema()

        return make_response(
            jsonify(schema.dump(data)),
            200
        )

    def post(self):
        """Framework Template view
        ---
        description: Create a Framework Template
        parameters:
        - in: body
          name: body
          required: true
          schema: FrameworkTemplateParams
        responses:
          200:
            content:
              application/json:
                schema: FrameworkTemplateParams
        """
        payload = request.get_json()

        try:
            schema = FrameworkTemplateSchema()
            framework_template = schema.load(payload)
        except ValidationError as err:
            return jsonify(err.messages)

        db.add(framework_template)
        db.commit()

        return make_response(
            jsonify(success=True),
            200
        )
