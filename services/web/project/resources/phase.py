from marshmallow import ValidationError

from flask import (
    jsonify,
    make_response
)
from flask_restful import Resource, request, fields, marshal_with

from project.database import Session
from project.models.framework_template import Phase, PhaseSchema

from project.resources import helpers

db = Session()


class PhaseEndpoint(Resource):

    def get(self, phase_id):
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

        try:
            schema = PhaseSchema()
            phases = schema.load(payload, many=True)
        except ValidationError as err:
            return jsonify(err.messages)

        db.add_all(phases)
        db.commit()

        return make_response(jsonify(success=True), 200)
