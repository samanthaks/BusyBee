from app import db
from flask.ext.mongoengine.wtf import model_form 

class Request(db.Document):
    title = db.StringField(required=True, max_length=200)
    author = db.StringField(required=True, max_length=100)
    details = db.StringField(required=True)
    runner = db.IntField()
    pick_up = db.StringField(required=True)
    drop_off = db.StringField(required=True)
    weight = db.DecimalField()
    status = db.IntField()


RequestForm= model_form(Request)
