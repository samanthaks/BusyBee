from flask import Blueprint, request, redirect, render_template, url_for, flash, current_app
from app import lm, flask_bcrypt
from flask_login import login_user, logout_user, login_required
#from app.models.login_form_model import LoginForm

#from app.User import UserSub
from app.models.user_model import User, SignupForm  #, LoginForm


user = Blueprint('users', __name__, template_folder='../templates')

"""
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
"""


@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        userObj = User()
        user = userObj.get_by_email_w_password(email)
        if user and flask_bcrypt.check_password_hash(user.password, request.form["password"]) and user.is_active():
            remember = request.form.get("remember", "no") == "yes"

            if login_user(user, remember=remember):
                flash("Logged in!")
                return redirect('/')
            else:
                flash("unable to log you in")

    return render_template("/login.html")


@user.route("/register", methods=["GET", "POST"])
def register():
    
    registerForm = SignupForm(request.form)
    current_app.logger.info(request.form)

    if request.method == 'POST' and registerForm.validate() == False:
        current_app.logger.info(registerForm.errors)
        return "registration error"

    elif request.method == 'POST' and registerForm.validate():
        email = request.form['email']

        # generate password hash
        password_hash = flask_bcrypt.generate_password_hash(request.form['password'])

        # prepare User
        user = User(email=email, password=password_hash)
        print user
        print email
        print password_hash

        try:
            user.save()
            print "saved"
            if login_user(user, remember="no"):
                flash("Logged in!")
                return redirect('/')
            else:
                flash("unable to log you in")

        except:
            flash("unable to register with that email address")
            current_app.logger.error("Error on registration - possible duplicate emails")

    # prepare registration form         
    registerForm = SignupForm(csrf_enabled=True)
    templateData = {

        'form' : registerForm
    }

    return render_template("/register.html", **templateData)


@user.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/login')


@lm.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@lm.user_loader
def load_user(id):
    if id is None:
        redirect('/login')
    user = User()
    user.get_by_id(id)
    if user.is_active():
        return user
    else:
        return None
