from marshmallow import ValidationError

from flask import (
    jsonify,
    make_response
)
from flask_restful import Resource, request, fields, marshal_with

from project.database import Session
from project.models.framework_template import FrameworkTemplate, FrameworkTemplateSchema
from project.resources import helpers

db = Session()


class FrameworkTemplateEndpoint(Resource):

    def get(self, framework_template_id):
        args = request.args
        data = db.query(FrameworkTemplate).get(framework_template_id)
        only_fields = helpers.get_only_fields(args)

        if only_fields:
            schema = FrameworkTemplateSchema(only=(only_fields))
        else:
            schema = FrameworkTemplateSchema()

        return schema.dump(data)

    def put(self, framework_template_id):
        payload = request.get_json()

        try:
            schema = FrameworkTemplateSchema()
            data = schema.load(payload, partial=True)
        except ValidationError as err:
            return jsonify(err.messages)

        db.query(FrameworkTemplate).filter_by(
            id=framework_template_id
        ).update(schema.dump(data))
        db.commit()

        return make_response(jsonify(success=True), 200)

    def post(self):
        payload = request.get_json()

        try:
            schema = FrameworkTemplateSchema()
            framework_template = schema.load(payload)
        except ValidationError as err:
            return jsonify(err.messages)

        db.add(framework_template)
        db.commit()

        return make_response(jsonify(success=True), 200)


class FrameworkTemplatesEndpoint(Resource):

    def get(self):
        args = request.args
        framework_templates = db.query(FrameworkTemplate).all()
        only_fields = helpers.get_only_fields(args)

        if only_fields:
            schema = FrameworkTemplateSchema(many=True, only=(only_fields))
        else:
            schema = FrameworkTemplateSchema(many=True)

        return schema.dump(framework_templates)
