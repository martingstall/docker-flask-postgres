from marshmallow import ValidationError

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request
)

from project.database import Session
from project.models.framework_template import FrameworkTemplate, FrameworkTemplateSchema
from project.models.framework_template import FrameworkTemplateParams
from project.resources import helpers

db = Session()

bp = Blueprint('framework_template', __name__, url_prefix='/framework_template_bp')


@bp.route('/<framework_template_id>', methods=('GET',))
def single_framework_template(framework_template_id):
    """Get a Framework Template.
    ---
    get:
      description: Get a Framework Template
      parameters:
        - in: path
          name: framework_template_id
          required: true
          schema:
            type: integer
          description: The framework template ID
        - in: query
          name: fields
          schema:
            type: string
          description: Limit what data is returned
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: FrameworkTemplateSchema
    """
    args = request.args
    data = db.query(FrameworkTemplate).get(framework_template_id)
    only_fields = helpers.get_only_fields(args)

    if only_fields:
        schema = FrameworkTemplateSchema(only=(only_fields))
    else:
        schema = FrameworkTemplateSchema()

    return make_response(
        jsonify(schema.dump(data)),
        200
    )


@bp.route('/create', methods=('POST',))
def create_framework_template():
    """Create a new Framework Template.
    ---
    post:
      summary: Create a new Framework Template
      requestBody:
        description: Framework Template to be added
        required: true
        content:
          application/json:
            schema: FrameworkTemplateParams
      responses:
        200:
          description: OK
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


@bp.route('/<framework_template_id>', methods=('PUT',))
def update_framework_template(framework_template_id):
    """Get a Framework Template.
    ---
    put:
      description: Update a Framework Template
      parameters:
        - in: path
          name: framework_template_id
          required: true
          schema:
            type: integer
          description: The framework template ID
      responses:
        200:
          description: Return a pet
          content:
            application/json:
              schema: FrameworkTemplateSchema
    """
    payload = request.get_json()

    try:
        schema = FrameworkTemplateSchema()
        schema.load(payload, partial=True)
    except ValidationError as err:
        return jsonify(err.messages)

    db.query(FrameworkTemplate).filter_by(
        id=framework_template_id
    ).update(payload)
    db.commit()

    return make_response(
        jsonify(success=True),
        200
    )


@bp.route('/by_client/<client_id>', methods=('GET',))
def by_client(client_id):
    """Get all Framework Templates that belong to the specified client.
    ---
    get:
      description: Get all Framework Templates that belong to the specified client
      parameters:
        - in: path
          name: client_id
          required: true
          schema:
            type: integer
          description: The client ID
      responses:
        200:
          description: Return a list of Framework Templates
          content:
            application/json:
              schema: FrameworkTemplateSchema
    """
    args = request.args
    data = db.query(FrameworkTemplate).all()
    only_fields = helpers.get_only_fields(args)

    if only_fields:
        schema = FrameworkTemplateSchema(many=True, only=(only_fields))
    else:
        schema = FrameworkTemplateSchema(many=True)

    return make_response(
        jsonify(schema.dump(data)),
        200
    )
