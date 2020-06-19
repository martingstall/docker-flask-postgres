from marshmallow import ValidationError

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request
)

from project.database import Session
from project.models.framework_template import Phase, PhaseSchema
from project.models.framework_template import PhaseParams
from project.resources import helpers

db = Session()

bp = Blueprint('phase', __name__, url_prefix='/phase_bp')


@bp.route('/<phase_id>', methods=('GET',))
def single_phase(phase_id):
    """Get a Phase.
    ---
    get:
      description: Get a Phase
      parameters:
        - in: path
          name: phase_id
          required: true
          schema:
            type: integer
          description: The phase ID
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: PhaseSchema
    """
    args = request.args
    data = db.query(Phase).get(phase_id)
    only_fields = helpers.get_only_fields(args)

    if only_fields:
        schema = PhaseSchema(only=(only_fields))
    else:
        schema = PhaseSchema()

    return make_response(
        jsonify(schema.dump(data)),
        200
    )


@bp.route('/create', methods=('POST',))
def create_phase():
    """Create a new Phase.
    ---
    post:
      summary: Create a new Phase
      requestBody:
        description: Phase to be added
        required: true
        content:
          application/json:
            schema: PhaseParams
      responses:
        200:
          description: OK
    """
    payload = request.get_json()

    try:
        schema = PhaseSchema()
        phase = schema.load(payload)
    except ValidationError as err:
        return jsonify(err.messages)

    db.add(phase)
    db.commit()

    return make_response(
        jsonify(success=True),
        200
    )


@bp.route('/bulk_create', methods=('POST',))
def bulk_create():
    """Create multiple Phases.
    ---
    post:
      summary: Create multiple Phases
      requestBody:
        description: List of Phases to be added
        required: true
        content:
          application/json:
            schema: PhaseParams
      responses:
        200:
          description: OK
    """
    payload = request.get_json()

    try:
        schema = PhaseSchema()
        phases = schema.load(payload, many=True)
    except ValidationError as err:
        return jsonify(err.messages)

    db.add_all(phases)
    db.commit()

    return make_response(
        jsonify(success=True),
        200
    )


@bp.route('/<phase_id>', methods=('PUT',))
def update_phase(phase_id):
    """Get a Phase.
    ---
    put:
      description: Update a Phase
      parameters:
        - in: path
          name: phase_id
          required: true
          schema:
            type: integer
          description: The phase ID
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: PhaseSchema
    """
    payload = request.get_json()

    try:
        schema = PhaseSchema()
        schema.load(payload, partial=True)
    except ValidationError as err:
        return jsonify(err.messages)

    db.query(Phase).filter_by(
        id=phase_id
    ).update(payload)
    db.commit()

    return make_response(
        jsonify(success=True),
        200
    )


@bp.route('/by_framework_template/<framework_template_id>', methods=('GET',))
def by_framework_templates(framework_template_id):
    """Get all Framework Templates that belong to the specified client.
    ---
    get:
      description: Get all Phases that belong to the specified Framework Template
      parameters:
        - in: path
          name: framework_template_id
          required: true
          schema:
            type: integer
          description: The phase ID
      responses:
        200:
          description: Return a list of Phases
          content:
            application/json:
              schema: PhaseSchema
    """
    args = request.args
    data = db.query(Phase).filter_by(
        framework_template_id=framework_template_id
    )
    only_fields = helpers.get_only_fields(args)

    if only_fields:
        schema = PhaseSchema(many=True, only=(only_fields))
    else:
        schema = PhaseSchema(many=True)

    return make_response(
        jsonify(schema.dump(data)),
        200
    )
