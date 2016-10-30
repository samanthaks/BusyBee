from app import db
from flask_mongoengine.wtf import model_form


class User(db.Document):
    username = db.StringField(required=True, max_length=15)
    password = db.StringField(required=True, max_length=20)
    email = db.StringField(required=True)
    requests_made = db.ListField(required=True)


UserForm = model_form(User)
