import os

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for,
    render_template
)

from flask_restful import Resource, Api

from project.apispec_v2 import spec_v2

from project.blueprints import framework_template, phase, step

from project.method_views.framework_template import FrameworkTemplate as FrameworkTemplateMV

from project.resources.framework_template import FrameworkTemplateEndpoint, FrameworkTemplatesEndpoint
from project.resources.phase import PhaseEndpoint, PhasesEndpoint

app = Flask(__name__)
app.config.from_object("project.config.Config")
api = Api(app)

app.register_blueprint(framework_template.bp)
app.register_blueprint(phase.bp)
app.register_blueprint(step.bp)

with app.test_request_context():
    spec_v2.path(view=framework_template.single_framework_template)
    spec_v2.path(view=framework_template.create_framework_template)
    spec_v2.path(view=framework_template.update_framework_template)
    spec_v2.path(view=framework_template.by_client)
    spec_v2.path(view=phase.single_phase)
    spec_v2.path(view=phase.create_phase)
    spec_v2.path(view=phase.bulk_create)
    spec_v2.path(view=phase.update_phase)
    spec_v2.path(view=phase.by_framework_templates)
    spec_v2.path(view=step.single_step)
    spec_v2.path(view=step.create_step)
    spec_v2.path(view=step.update_step)
    spec_v2.path(view=step.by_phases)

method_view = FrameworkTemplateMV.as_view('framework_template_mv')
app.add_url_rule(
    '/framework_template_mv/<framework_template_id>',
    view_func=method_view,
    methods=['GET',]
)
app.add_url_rule(
    '/framework_template_mv/',
    view_func=method_view,
    methods=['POST',]
)
"""
# Per their docs... this doesn't work with multiple add_url_rule()
app.add_url_rule('/framework_template_mv/<framework_template_id>', view_func=method_view)
with app.test_request_context():
    spec_v2.path(view=method_view)
"""

api.add_resource(
    FrameworkTemplateEndpoint,
    '/frameworktemplate',
    '/frameworktemplate/<int:framework_template_id>',
)

api.add_resource(
    FrameworkTemplatesEndpoint,
    '/frameworktemplates',
)

api.add_resource(
    PhaseEndpoint,
    '/phase',
    '/phase/<int:phase_id>',
)

api.add_resource(
    PhasesEndpoint,
    '/phases',
    '/phases/<int:framework_template_id>',
)


@app.route("/api/docs")
def api_docs():
    return jsonify(spec_v2.to_dict())


@app.route("/")
def hello_world():
    return jsonify(hello="world 2")


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return f"""
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """
