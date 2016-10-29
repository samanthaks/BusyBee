from app import db


class User(db.Document):
    username = db.StringField(required=True, max_length=15)
    password = db.StringField(required=True, max_length=20)
    requests_made = db.ListField(required=True)
