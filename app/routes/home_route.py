"""Home Route"""
from flask import Blueprint, render_template, session

home = Blueprint('home', __name__, template_folder='../templates')


@home.route('/')
def home_page():
    """The home page."""
    if 'Username' in session:
        return render_template('user_index.html')
    return render_template('index.html')
