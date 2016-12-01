from flask import Blueprint, request, redirect, render_template, url_for, \
                    flash, session, current_app
from app.models.user_model import User, UserForm, db
from werkzeug.security import generate_password_hash
from app.models.task_model import Request


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


@user.route('/user/<username>')
def view_profile(username):
    if 'Username' in session:
        user = User.objects.get_or_404(Username=username)
        tasks = Request.objects(db.Q(author=session['Username'],status=3) | db.Q(runner=session['Username'],status=3))
        tasks_authored = Request.objects(author=session['Username'],status=3)
        tasks_ran = Request.objects(runner=session['Username'],status=3)
        num_ran = len(tasks_ran)
        return render_template('profile.html', user=user, tasks=tasks, tasks_authored=tasks_authored, tasks_ran=tasks_ran, num_ran=num_ran)
    flash("You need to be logged in to access this page", category='error')
    return redirect(url_for("users.login"))
