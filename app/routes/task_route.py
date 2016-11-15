from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.models.task_model import Request, RequestForm
from flask_login import current_user, login_required
from printdebug import printobject, debug
from app import app


tasks = Blueprint('tasks', __name__, template_folder='../templates')


@tasks.route('/tasks')
def tasks_page():
    """The main tasks page"""
    if 'Username' in session:
        requests = Request.objects()
        return render_template('tasks.html', tasks=requests)
    flash("You need to be logged in to access this page", category='error')
    return redirect(url_for("users.login"))


@tasks.route('/new_task', methods=['GET', 'POST'])
def new_task():
    """Create a new post"""
    if 'Username' in session:
        form = RequestForm(request.form)
        form.author.data = session['Username']
        form.status.data = 0

        if request.method == 'POST' and form.validate():
            form.save()
            return redirect(url_for('tasks.tasks_page'))

        return render_template('new_task.html', form=form)
    flash("You need to be logged in to access this page", category='error')
    return redirect(url_for("users.login"))


@tasks.route('/view', methods=['GET', 'POST'])
def view():
    """View and edit tasks"""
    if 'Username' in session:
        id = request.args.get('id')
        task = Request.objects.get_or_404(id=id)

        status = request.args.get('status')
        if status is not None:
            status = int(status)
            if status == 0:
                Request.objects(id=id).update(status=1)
                Request.objects(id=id).update(runner=session['Username'])

            if status == 1:
                Request.objects(id=id).update(status=2)

            if status == 2:
                Request.objects(id=id).update(status=3)
            return redirect(url_for('tasks.view', id=task.id))
        return render_template('task_post.html', tasks=task, user=session['Username'])
    flash("You need to be logged in to access this page", category='error')
    return redirect(url_for("users.login"))
