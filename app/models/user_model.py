"""user_model.py"""
from app import db
from werkzeug.security import check_password_hash
from flask_mongoengine.wtf import model_form


class User(db.Document):
    """Create user class"""
    Email = db.EmailField(required=True)
    Username = db.StringField(required=True, max_length=50)
    Password = db.StringField(required=True, max_length=100)

    def __init__(self, Username=None, Email=None, Password=None,
                 *args, **kwargs):
        super(db.Document, self).__init__(*args, **kwargs)
        self.Username = Username
        self.Password = Password
        self.Email = Email
        self.is_authenticated = False

    @staticmethod
    def validate_login(password_hash, password):
        """validate password"""
        return check_password_hash(password_hash, password)


UserForm = model_form(User)
