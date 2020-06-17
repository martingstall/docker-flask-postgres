from pprint import pprint

from flask import (
    jsonify,
)
from flask_restful import Resource, request, fields, marshal_with

from project.database import Session
from project.models.framework_template import Phase, PhaseSchema

from project.resources import helpers

db = Session()


class PhaseEndpoint(Resource):

    def get(self, phase_id, **kwargs):
        args = request.args
        phase = db.query(Phase).get(phase_id)
        only_fields = helpers.get_only_fields(args)

        if only_fields:
            schema = PhaseSchema(only=(only_fields))
        else:
            schema = PhaseSchema()

        return schema.dump(phase)

    def put(self, phase_id):
        payload = request.get_json()
        phase = db.query(Phase).get(phase_id)
        phase.name = payload.get('phase_name')
        db.commit()

        return jsonify({"phase_id": phase_id})

    def post(self):
        payload = request.get_json()
        phase = Phase(
            name=payload.get('phase_name')
        )
        db.add(phase)
        db.commit()

        return jsonify({})


class PhasesEndpoint(Resource):

    def get(self):
        args = request.args
        phases = db.query(Phase).all()
        only_fields = helpers.get_only_fields(args)

        if only_fields:
            schema = PhaseSchema(many=True, only=(only_fields))
        else:
            schema = PhaseSchema(many=True)

        return schema.dump(phases)

    def post(self):
        payload = request.get_json()
        for row in payload:
            print("")
            print("")
            print("ROW: ", row)
            print("")
            print("")

        return jsonify({})