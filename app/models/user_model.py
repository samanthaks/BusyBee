from app import db
#from werkzeug.security import check_password_hash
from flask_mongoengine.wtf import model_form
from flask_mongoengine.wtf.orm import validators
from wtforms.fields import PasswordField


class User(db.Document):
    #username = db.StringField(required=True, max_length=20, unique=True)
    email = db.EmailField(required=True)
    password = PasswordField(required=True, max_length=20)
    active = db.BooleanField(default=True)

    def get_by_email_w_password(self, emails):

        try:
            print "hello"
            dbUser = self.objects.get(email=emails)
            
            if dbUser:
                print "dbUser exists"
                email = dbUser.email
                #self.active = dbUser.active
                password = dbUser.password
                #self.id = dbUser.id
                return self
            else:
                return None
        except:
            print "there was an error"
            return None

    

    def __init__(self, email=None, password=None, active=True):
        email = email
        password = password
        active = active
        #self.isAdmin = False
        #self.id = None

    """    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

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
"""

user_form = model_form(User, exclude=['password'])


class SignupForm(user_form):
    password = PasswordField('Password', validators=[validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


# Login form will provide a Password field (WTForm form field)
class LoginForm(user_form):
    password = PasswordField('Password', validators=[validators.Required()])
