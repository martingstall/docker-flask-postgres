from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from wtforms_sqlalchemy.orm import model_form

from project.models.shared import db
from project.models.users import User

from project.forms.users import MyFlaskForm

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/create/', methods=('GET', 'POST'))
def create_user():
    """
    form = MyFlaskForm()
    if form.validate_on_submit():
        return redirect('/list/')
    """
    user = User()
    data = {
        "form_errors": []
    }
    success = False
    UserForm = model_form(User)

    if request.method == 'POST':
        form = UserForm(request.form, obj=user)
        if form.validate():
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            success = True
        else:
            print ("FORM ERRORS: ", form.errors)
            data["form_errors"] = form.errors
    else:
        form = UserForm(obj=user)

    data["success"] = success
    data["form"] = form

    return render_template('users/create.html', data=data)


@bp.route('/<int:user_id>/edit/', methods=('GET', 'POST'))
def edit_user(user_id):
    print ("user_id: ", user_id)
    pass
    #user = db.session.query(User).filter(User.id == id)


@bp.route('/list/', methods=('GET', 'POST'))
def list_users():
    data = {
        "users": db.session.query(User)
    }
    return render_template('users/list_users.html', data=data)
