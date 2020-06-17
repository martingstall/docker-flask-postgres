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

from project.resources.framework_template import FrameworkTemplateEndpoint, FrameworkTemplatesEndpoint
from project.resources.phase import PhaseEndpoint, PhasesEndpoint

app = Flask(__name__)
app.config.from_object("project.config.Config")
api = Api(app)

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
