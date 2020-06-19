from marshmallow import ValidationError

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request
)

from project.database import Session
from project.models.framework_template import Step, StepSchema
from project.models.framework_template import StepParams
from project.resources import helpers

db = Session()

bp = Blueprint('step', __name__, url_prefix='/step_bp')


@bp.route('/<step_id>', methods=('GET',))
def single_step(step_id):
    """Get a Step.
    ---
    get:
      description: Get a Step
      parameters:
        - in: path
          name: step_id
          required: true
          schema:
            type: integer
          description: The step ID
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: StepSchema
    """
    args = request.args
    data = db.query(Step).get(step_id)
    only_fields = helpers.get_only_fields(args)

    if only_fields:
        schema = StepSchema(only=(only_fields))
    else:
        schema = StepSchema()

    return make_response(
        jsonify(schema.dump(data)),
        200
    )


@bp.route('/create', methods=('POST',))
def create_step():
    """Create a new Step.
    ---
    post:
      summary: Create a new Step
      requestBody:
        description: Step to be added
        required: true
        content:
          application/json:
            schema: StepParams
      responses:
        200:
          description: OK
    """
    payload = request.get_json()

    try:
        schema = StepSchema()
        step = schema.load(payload)
    except ValidationError as err:
        return jsonify(err.messages)

    db.add(step)
    db.commit()

    return make_response(
        jsonify(success=True),
        200
    )


@bp.route('/<step_id>', methods=('PUT',))
def update_step(step_id):
    """Get a Step.
    ---
    put:
      description: Update a Step
      parameters:
        - in: path
          name: step_id
          required: true
          schema:
            type: integer
          description: The step ID
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: StepSchema
    """
    payload = request.get_json()

    try:
        schema = StepSchema()
        schema.load(payload, partial=True)
    except ValidationError as err:
        return jsonify(err.messages)

    db.query(Step).filter_by(
        id=step_id
    ).update(payload)
    db.commit()

    return make_response(
        jsonify(success=True),
        200
    )


@bp.route('/by_phase/<phase_id>', methods=('GET',))
def by_phases(phase_id):
    """Get all Steps that belong to the specified Phase.
    ---
    get:
      description: Get all Steps that belong to the specified Phase
      parameters:
        - in: path
          name: phase_id
          required: true
          schema:
            type: integer
          description: The step ID
      responses:
        200:
          description: Return a list of Steps
          content:
            application/json:
              schema: StepSchema
    """
    args = request.args
    data = db.query(Step).filter_by(
        phase_id=phase_id
    )
    only_fields = helpers.get_only_fields(args)

    if only_fields:
        schema = StepSchema(many=True, only=(only_fields))
    else:
        schema = StepSchema(many=True)

    return make_response(
        jsonify(schema.dump(data)),
        200
    )
