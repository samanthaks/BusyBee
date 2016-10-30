from flask import Blueprint, render_template, redirect, url_for, request
from app.models.request_model import Request, RequestForm


tasks = Blueprint('tasks', __name__, template_folder='../templates')


@tasks.route('/tasks')
def tasks_page():
    """The main tasks page"""
    requests = Request.objects()
    return render_template('tasks.html', tasks=requests)


@tasks.route('/new', methods=['GET', 'POST'])
def new_task():
    """Create a new post"""
    form = RequestForm(request.form)

    if request.method == 'POST' and form.validate():
        form.save()
        return redirect(url_for('tasks.tasks_page'))

    return render_template('new_task.html', form=form)


@tasks.route('/view', methods=['GET','POST'])
def view():
	"""View  tasks)"""
	id = request.args.get('id')
	task = Request.objects.get_or_404(id=id)

	status = request.args.get('status')
	if status != None:
		status = int(status)
		if status == 0:
			Request.objects(id=id).update(status=1)
			Request.objects(id=id).update(runner=1)

		if status == 1:
			Request.objects(id=id).update(status=2)

	return render_template('task_post.html', tasks=task)

