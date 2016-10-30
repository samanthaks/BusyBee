from flask import Blueprint, render_template, redirect, url_for, request 
from app.models.request import Request, RequestForm


tasks = Blueprint('tasks', __name__, template_folder='../templates')


@tasks.route('/tasks')
def tasks_page():
    """The main tasks page"""
    request = Request.objects()
    return render_template('tasks.html', tasks=request)


@tasks.route('/new', methods=['GET', 'POST'])
def new():
    """Create a new post"""
    form = RequestForm(request.form)

    if request.method == 'POST' and form.validate():
        form.save()
        return redirect(url_for('tasks.tasks_page'))

    return render_template('new.html', form=form)
