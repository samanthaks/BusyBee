from app import login_manager
from flask import Blueprint, request, redirect, render_template, url_for, \
                    flash, session, g
from flask_login import login_user, logout_user, current_user
from app.models.user_model import User, UserForm
from printdebug import debug, printobject
from werkzeug.security import generate_password_hash


user = Blueprint('users', __name__, template_folder='../templates')


@user.route('/users')
def tasks_page():
    """The main tasks page"""
    users = User.objects()
    return render_template('users.html', users=users)


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        form.password.data = generate_password_hash(form.password.data)
        form.save()
        flash('Thanks for registering. Please Log In')
        return redirect(url_for('users.login'))
    else:
        return render_template('signup.html', title='sign up', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm(request.form)

    if request.method == 'POST':
        try:
            user = User.objects.get(username=form.username.data)

            if user and user.validate_login(user.password, form.password.data):
                user_obj = User(user.username)
                login_user(user_obj, remember=True)
                session['logged_in'] = True
                session['username'] = user.username
                session.permanent = True
                flash("Logged in successfully! " + current_user.username, category='success')
                next = request.args.get('next')
                return redirect(next or url_for("tasks.tasks_page"))
            flash("Wrong username or password!", category='error')
        except User.DoesNotExist:
            flash("User does not exist. Please Sign Up ")
    return render_template('login.html', title='login', form=form)


@user.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('users.login'))


@login_manager.user_loader
def load_user(username):
    try:
        return User.get(username=username)
    except:
        return None


@user.before_request
def before_request():
    g.user = current_user
