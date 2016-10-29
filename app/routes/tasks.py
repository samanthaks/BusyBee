from flask import Blueprint, render_template
from app.models.request import Request


tasks = Blueprint('tasks', __name__, template_folder='../templates')


@tasks.route('/tasks')
def tasks_page():
    """The main tasks page"""
    request = Request.objects()
    return render_template('tasks.html', tasks=request)
