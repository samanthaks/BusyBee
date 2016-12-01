""" run using "python app.py" """
from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

db = MongoEngine()

def create_app(MONGO={'db': 'BusyBee'},
               TESTING=False,
               CSRF_ENABLED=False,
               WTF_CSRF_ENABLED=False):
    """Create app using config variables"""
    app = Flask(__name__)

    app.config["DEBUG"] = True
    app.config["TESTING"] = TESTING
    app.config['MONGODB_SETTINGS'] = MONGO
    app.config['CSRF_ENABLED'] = CSRF_ENABLED
    app.config['WTF_CSRF_ENABLED'] = WTF_CSRF_ENABLED
    app.config['SECRET_KEY'] = 'X{WC3JsG6m7m4o8W3DwrrgJ0[Np,!O'
    app.config['DEBUG_TB_PANELS'] = ['flask_mongoengine.panels.MongoDebugPanel']
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


    # Setup the database.
    db.init_app(app)
    app.session_interface = MongoEngineSessionInterface(db)
    toolbar = DebugToolbarExtension(app)

    from app.routes.home_route import home
    from app.routes.task_route import tasks
    from app.routes.user_route import user

    app.register_blueprint(home)
    app.register_blueprint(tasks)
    app.register_blueprint(user)

    return app
