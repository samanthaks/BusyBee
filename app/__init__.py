""" run using "python app.py" """
from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect
from flask_login import LoginManager


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MONGODB_SETTINGS'] = {'db': 'BusyBee'}
app.config['SECRET_KEY'] = 'X{WC3JsG6m7m4o8W3DwrrgJ0[Np,!O'
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

db = MongoEngine(app)

from app.routes.home_route import home
from app.routes.task_route import tasks
from app.routes.user_route import user
"""from app.routes.new import new"""

app.register_blueprint(home)
app.register_blueprint(tasks)
app.register_blueprint(user)
"""app.register_blueprint(new)"""
