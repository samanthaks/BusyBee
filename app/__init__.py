""" run using "python app.py" """
from flask import Flask
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MONGODB_SETTINGS'] = {'db': 'BusyBee'}
app.config['SECRET_KEY'] = 'X{WC3JsG6m7m4o8W3DwrrgJ0[Np,!O'

db = MongoEngine(app)


from app.routes.home import home
from app.routes.tasks import tasks

app.register_blueprint(home)
app.register_blueprint(tasks)
