from app import db
from werkzeug.security import check_password_hash
from flask_mongoengine.wtf import model_form


class User(db.Document):
    email = db.StringField(required=True)
    username = db.StringField(required=True)
    password = db.StringField(required=True)

    def __init__(self, username=None, email=None, password=None, *args, **kwargs):
        super(db.Document, self).__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.email = email
        self.is_authenticated = False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

UserForm = model_form(User)
