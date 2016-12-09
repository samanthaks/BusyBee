"""User Functions"""
from flask import Blueprint, request, redirect, render_template, url_for, \
                    flash, session
from app.models.user_model import User, UserForm, db
from app.models.task_model import Request
from werkzeug.security import generate_password_hash


user = Blueprint('users', __name__, template_folder='../templates')


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign up"""
    form = UserForm(request.form)
    if request.method == 'GET':
        return render_template('signup.html', title='sign up', form=form)
    if request.method == 'POST':
        if 'Username' in session:
            flash("You are already logged in! If you would like to log in as another user, please log out first!", category='error')
            return render_template('login_loggedin.html', title='login', form=form)
        if form.validate():
            try:
                if User.objects.get(Username=form.Username.data):
                    flash("Username already exists, choose another!", category='error')
                    return render_template('signup.html', title='login', form=form)
            except User.DoesNotExist:
                try:
                    if User.objects.get(Email=form.Email.data):
                        flash("Email already exists, choose another!", category='error')
                        return render_template('signup.html', title='login', form=form)
                except User.DoesNotExist:
                    form.Password.data = generate_password_hash(form.Password.data)
                    form.save()
                    flash('Thanks for registering. Please Log In', category='success')
                    return redirect(url_for('users.login'))
        else:
            for errors in form.errors.items():
                flash("Invalid Email Address", category='error')
            return render_template('signup.html', title='sign up', form=form)

@user.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    form = UserForm(request.form)
    if request.method == 'POST':
        if 'Username' in session:
            flash("You are already logged in! If you would like to log in as another user, please log out first!", category='error')
            return render_template('login_loggedin.html', title='login', form=form)
        try:
            user_query = User.objects.get(Username=form.Username.data)

            if user_query and user_query.validate_login(user_query.Password, form.Password.data):
                session['Username'] = user_query.Username
                flash("Logged in successfully!", category='success')
                return redirect(request.args.get('next') or url_for("home.home_page"))
            flash("Wrong password!", category='error')
        except User.DoesNotExist:
            flash("User does not exist. Please Sign Up", category='error')
    return render_template('login.html', title='login', form=form)


@user.route('/logout')
def logout():
    """User Logout"""
    session.clear()
    flash("You were logged out!", category='success')
    return redirect(url_for('users.login'))


@user.route('/user/<username>')
def view_profile(username):
    """View user profile"""
    if 'Username' in session:
        user = User.objects.get_or_404(Username=username)
        tasks = Request.objects(db.Q(author=username, status=3) | db.Q(runner=username, status=3))
        num_ran = len(Request.objects(runner=username, status=3))
        return render_template('profile.html', user=user, tasks=tasks, num_ran=num_ran)
    flash("You need to be logged in to access this page", category='error')
    return redirect(url_for("users.login"))
