from flask import Blueprint, request, redirect, render_template, url_for, \
                    flash, session, current_app
from app.models.user_model import User, UserForm
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
        try:
            if(User.objects.get(Username=form.Username.data)):
                flash("Username already exists, choose another!", category='error')
                return render_template('signup.html', title='login', form=form)
        except User.DoesNotExist:
            try:
                if (User.objects.get(Email=form.Email.data)):
                    flash("Email already exists, choose another!", category='error')
                    return render_template('signup.html', title='login', form=form)
            except User.DoesNotExist:
                form.Password.data = generate_password_hash(form.Password.data)
                form.save()
                flash('Thanks for registering. Please Log In', category='success')
                return redirect(url_for('users.login'))
    else:
        return render_template('signup.html', title='sign up', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm(request.form)

    if request.method == 'POST':
        try:
            user = User.objects.get(Username=form.Username.data)

            if user and user.validate_login(user.Password, form.Password.data):
                session['Username'] = user.Username
                flash("Logged in successfully!", category='success')
                next = request.args.get('next')
                return redirect(next or url_for("home.home_page"))
            flash("Wrong password!", category='error')
        except User.DoesNotExist:
            flash("User does not exist. Please Sign Up", category='error')
    return render_template('login.html', title='login', form=form)


@user.route('/logout')
def logout():
    session.clear()
    flash("You were logged out!", category='success')
    return redirect(url_for('users.login'))
