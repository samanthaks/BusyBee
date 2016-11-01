""" run using "python app.py" """
from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MONGODB_SETTINGS'] = {'db': 'BusyBee'}
app.config['SECRET_KEY'] = 'X{WC3JsG6m7m4o8W3DwrrgJ0[Np,!O'
app.config['DEBUG_TB_PANELS'] = ['flask_mongoengine.panels.MongoDebugPanel']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.session_protection = "strong"

db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)
toolbar = DebugToolbarExtension(app)


from app.routes.home_route import home
from app.routes.task_route import tasks
from app.routes.user_route import user
"""from app.routes.new import new"""

app.register_blueprint(home)
app.register_blueprint(tasks)
app.register_blueprint(user)
"""app.register_blueprint(new)"""
