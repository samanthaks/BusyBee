from app import lm
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.login_form_model import LoginForm
from app.models.user_model import User

user = Blueprint('users', __name__, template_folder='../templates')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("tasks.html"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@user.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    return render_template('new_task.html')


@user.route('/accept_task', methods=['GET', 'POST'])
@login_required
def accept_task():
    return render_template('accept_task.html')


@lm.user_loader
def load_user(username):
    u = user.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
