from app import db
from flask_mongoengine.wtf import model_form


class Request(db.Document):
    title = db.StringField(required=True, max_length=200)
    author = db.StringField(required=True, max_length=100)
    details = db.StringField(required=True, max_length=1000)
    runner = db.StringField()
    pick_up = db.StringField(required=True, max_length=1000)
    drop_off = db.StringField(required=True, max_length=1000)
    weight = db.DecimalField(required=True)
    status = db.IntField(required=True)
    runner_rating = db.DecimalField(min_value=0.0, max_value=5.0)
    runner_comment = db.StringField(max_length=1000)
    author_rating = db.DecimalField(min_value=0.0, max_value=5.0)
    author_comment = db.StringField(max_length=1000)


RequestForm = model_form(Request)
