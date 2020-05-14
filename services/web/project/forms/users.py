from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.orm import model_form

from project.models.users import User


class MyFlaskForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
