from flask import Blueprint, render_template, redirect, url_for
from app.models.user import UserForm

user = Blueprint('name', __name__, template_folder='../templates')


@user.route('/', methods=['GET', 'POST'])
def login_page():
    """The home page."""
    form = UserForm(user.form)

    if user.method == 'POST' and form.validate():
        form.save()
        return redirect(url_for('tasks.tasks_page'))

    return render_template('new.html', form=form)
