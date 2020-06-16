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

from project.models.shared import db
from project.models.users import User
from project.models.campaign import Campaign, Phase, Step

from project.blueprints import auth
from project.blueprints import user

from sqlalchemy.orm import load_only, subqueryload, joinedload

app = Flask(__name__)
app.config.from_object("project.config.Config")
api = Api(app)
db.init_app(app)

app.register_blueprint(auth.bp)
app.register_blueprint(user.bp)

TODOS = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        """
        data = Campaign.query.with_entities(
            Campaign.name,
            Phase.name
        ).all()
        """
        data = Campaign.query.get(todo_id)
        print (data)
        #data = Phase.query.all()
        #data = Step.query.all()
        return jsonify(data)
        #return {todo_id: TODOS[todo_id]}

    def put(self, todo_id):
        TODOS[todo_id] = request.form['data']
        return {todo_id: TODOS[todo_id]}


api.add_resource(
    TodoSimple,
    '/<string:todo_id>',
    '/<string:todo_id>/hithere/',
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
