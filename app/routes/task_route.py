from flask import Blueprint, render_template, redirect, url_for, request,\
                  session, flash, current_app, abort
from app.models.task_model import Request, RequestForm


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
            flash("Task successfully created!", category='success')
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
            if status == 0 and session['Username'] != task.author and task.status == 0:
                Request.objects(id=id).update(status=1)
                Request.objects(id=id).update(runner=session['Username'])
                flash("Task Status Updated: Assigned to " + session['Username'], category='success')

            elif status == 0 and session['Username'] == task.author:
                flash("You cannot assign yourself your own task", category='error')

            elif status == 0 and task.status == 1:
                flash("This task has already been assigned", category='error')

            elif status == 1 and session['Username'] == task.runner and task.status == 1:
                Request.objects(id=id).update(status=2)
                flash("Task Status Updated: Completed", category='success')

            elif status == 1 and session['Username'] != task.runner and task.status == 1:
                flash("You cannot update a task someone else is doing", category='error')

            elif status == 2 and session['Username'] == task.author and task.status == 2:
                Request.objects(id=id).update(status=3)
                flash("Task Status Updated: Completed & Accepted", category='success')

            elif status == 2 and session['Username'] == task.author and task.status == 3:
                flash("You have already marked this task Completed & Accepted", category='error')

            elif status == 2 and session['Username'] != task.author and task.status == 2:
                flash("Only the Task Author can mark this task Completed & Accepted", category='error')

            else:
                abort(404)

            return redirect(url_for('tasks.view', id=task.id))
        return render_template('task_post.html', tasks=task, user=session['Username'])
    flash("You need to be logged in to access this page", category='error')
    return redirect(url_for("users.login"))


@tasks.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
