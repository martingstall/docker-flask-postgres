from pprint import pprint

from flask import (
    jsonify,
)
from flask_restful import Resource, request

from project.database import Session
from project.models.campaign import Campaign, CampaignSchema, Phase, Step

from project.resources import helpers

db = Session()


class FrameworkTemplate(Resource):

    def get(self, framework_template_id):
        args = request.args
        obj = db.query(Campaign).get(framework_template_id)
        only_fields = helpers.get_only_fields(args)

        if only_fields:
            schema = CampaignSchema(only=(only_fields))
        else:
            schema = CampaignSchema()

        return schema.dump(obj)

    def put(self, framework_template_id):
        return jsonify({"put": framework_template_id})


class FrameworkTemplateList(Resource):

    def get(self):
        args = request.args
        objs = db.query(Campaign).all()
        only_fields = helpers.get_only_fields(args)

        if only_fields:
            schema = CampaignSchema(many=True, only=(only_fields))
        else:
            schema = CampaignSchema(many=True)

        return schema.dump(objs)
