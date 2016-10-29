from flask import Blueprint, render_template

home = Blueprint('name', __name__, template_folder='../templates')


@home.route('/')
def home_page():
    """The home page."""
    return render_template('index.html')