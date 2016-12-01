"""Task Routes"""
from flask import Blueprint, render_template, redirect, url_for, request,\
                  session, flash, abort
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
        task_id = request.args.get('id')
        task = Request.objects.get_or_404(id=task_id)

        if task.status == -1:
            abort(404)

        status = request.args.get('status')
        if status is not None:
            status = int(status)
            if status == 0 and session['Username'] != task.author and task.status == 0:
                Request.objects(id=task_id).update(status=1)
                Request.objects(id=task_id).update(runner=session['Username'])
                flash("Task Status Updated: Assigned to " + session['Username'], category='success')

            elif status == 0 and session['Username'] == task.author:
                flash("You cannot assign yourself your own task", category='error')

            elif status == 0 and task.status == 1:
                flash("This task has already been assigned", category='error')

            elif status == 1 and session['Username'] == task.runner and task.status == 1:
                Request.objects(id=task_id).update(status=2)
                flash("Task Status Updated: Completed", category='success')

            elif status == 1 and session['Username'] != task.runner and task.status == 1:
                flash("You cannot update a task someone else is doing", category='error')

            elif status == 2 and session['Username'] == task.author and task.status == 2:
                Request.objects(id=task_id).update(status=3)
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


@tasks.route('/write_review', methods=['GET', 'POST'])
def write_review():
    """Write runner or author review"""
    if 'Username' in session:
        id = request.args.get('id')
        task = Request.objects.get_or_404(id=id)

        if task.status == -1:
            abort(404)

        review_for = request.args.get('review_for')
        form = RequestForm(request.form)
        if request.method == 'POST':
            if review_for == "runner":
                if session['Username'] == task.author:
                    if form.runner_rating.data >= 0 and form.runner_rating.data <= 5.0 and task.runner_rating is None:
                        Request.objects(id=id).update(runner_rating=form.runner_rating.data)
                    else:
                        abort(404)
                    if form.runner_comment.data is not None and task.runner_comment is None:
                        Request.objects(id=id).update(runner_comment=form.runner_comment.data)
                    flash("Form Submitted!", category='success')
                    return redirect(url_for('tasks.view', id=id))
                else:
                    abort(404)

            elif review_for == "author":
                if session['Username'] == task.runner:
                    if form.author_rating.data >= 0 and form.author_rating.data <= 5.0 and task.author_rating is None:
                        Request.objects(id=id).update(author_rating=form.author_rating.data)
                    else:
                        abort(404)
                    if form.author_comment.data is not None and task.author_comment is None:
                        Request.objects(id=id).update(author_comment=form.author_comment.data)
                    flash("Form Submitted!", category='success')
                    return redirect(url_for('tasks.view', id=id))
                else:
                    abort(404)

        if request.method == 'GET' and review_for == "runner":
            if task.runner_rating is None:
                if session['Username'] == task.author:
                    return render_template('runner_review.html', form=form, review_for=review_for, id=id)
                else:
                    flash("You do not have access to this review", category='error')
                    return redirect(url_for('tasks.view', id=id))
            else:
                flash("Rating has already been submitted", category='error')
                return redirect(url_for('tasks.view', id=id))

        if request.method == 'GET' and review_for == "author":
            if task.author_rating is None:
                if session['Username'] == task.runner:
                    return render_template('author_review.html', form=form, review_for=review_for, id=id)
                else:
                    flash("You do not have access to this review", category='error')
                    return redirect(url_for('tasks.view', id=id))
            else:
                flash("Rating has already been submitted", category='error')
                return redirect(url_for('tasks.view', id=id))
    flash("You need to be logged in to access this page", category='error')
    return redirect(url_for("users.login"))


@tasks.route('/delete', methods=['GET'])
def remove():
    """Remove Request"""
    if 'Username' in session:
        id = request.args.get('id')
        task = Request.objects.get_or_404(id=id)

        if task.author == session['Username'] and task.status == 0:
            Request.objects(id=id).update(status=-1)
            flash("Task successfully deleted", category='success')
            return redirect(url_for('tasks.tasks_page'))
        else:
            abort(404)
    flash("You need to be logged in to access this page", category='error')
    return redirect(url_for("users.login"))


@tasks.errorhandler(404)
def page_not_found(error):
    """Displays 404"""
    return render_template('404.html'), 404
