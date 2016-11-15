from app import app
from app.models.user_model import User, UserForm
from app.models.task_model import Request, RequestForm
import flask
from flask_mongoengine import MongoEngine, get_connection
from mongoengine import connect
import unittest
from mock import MagicMock

class Test_Class(unittest.TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        connect('BusyBee', host='mongomock://localhost', alias='testdb')
        self.db = get_connection('testdb')

    def tearDown(self):
        get_connection('testdb').drop_collection('User')
        get_connection('testdb').drop_collection('Request')

    def test_non_user_pages(self):
        #check pages where user is not logged in 
        index_page = self.app.get('/')
        assert 'Welcome to BusyBee' in index_page.data

        login_page = self.app.get('/login')
        assert 'Username' in login_page.data
        assert 'Password' in login_page.data
        assert 'Sign In' in login_page.data
        assert 'Sign Up' in login_page.data

        signup_page = self.app.get('/signup')
        assert 'Username' in signup_page.data
        assert 'Password' in signup_page.data
        assert 'Email' in signup_page.data
        assert 'Submit' in signup_page.data

    def test_user(self):
        # Check valid credentials
        valid_signup = self.app.post('/signup', data=dict(Email='test1@test.com', Username='test1', Password='password'), follow_redirects=True)
        assert 'Thanks for registering. Please Log In' in valid_signup.data

        # Duplicate Email
        invalid_signup = self.app.post('/signup', data=dict(Email='test1@test.com', Username='test2', Password='password'), follow_redirects=True)
        assert 'Email already exists, choose another!' in invalid_signup.data

        # Duplicate Username
        invalid_signup = self.app.post('/signup', data=dict(Email='test2@test.com', Username='test1', Password='password'), follow_redirects=True)
        assert 'Username already exists, choose another!' in invalid_signup.data

        # invalid login - username
        invalid_login = self.app.post('/login', data=dict(Username='test123', Password='password2'), follow_redirects=True)
        assert '"User does not exist. Please Sign Up"' in invalid_login.data

        # invalid login - password
        invalid_login = self.app.post('/login', data=dict(Username='test1', Password='password2'), follow_redirects=True)
        assert 'Wrong password!' in invalid_login.data

        # valid login
        valid_login = self.app.post('/login', data=dict(Username='test1', Password='password'), follow_redirects=True)
        assert 'Logged in successfully!' in valid_login.data

        # Test log out
        logout = self.app.get('logout', follow_redirects=True)
        assert 'You were logged out!' in logout.data


    def test_tasks(self):
        # views w/o login
        invalid_view = self.app.get('/tasks', follow_redirects=True)
        assert 'You need to be logged in to access this page' in invalid_view.data

        invalid_view = self.app.get('/new_task', follow_redirects=True)
        assert 'You need to be logged in to access this page' in invalid_view.data

        invalid_view = self.app.get('/view', follow_redirects=True)
        assert 'You need to be logged in to access this page' in invalid_view.data

        # valid login
        valid_login = self.app.post('/login', data=dict(Username='test1', Password='password'), follow_redirects=True)
        assert 'Logged in successfully!' in valid_login.data

        # views w/ login
        valid_view = self.app.get('/tasks', follow_redirects=True)
        assert 'All Tasks' in valid_view.data

        valid_view = self.app.get('/new_task', follow_redirects=True)
        assert 'Post A New Request' in valid_view.data
        assert 'title' in valid_view.data
        assert 'details' in valid_view.data
        assert 'weight' in valid_view.data
        assert 'pick_up' in valid_view.data
        assert 'drop_off' in valid_view.data

        valid_view = self.app.get('/view', follow_redirects=True)
        assert 'Page Not Found' in valid_view.data


        # Test posting task
        new_task = self.app.post('/new_task', data=dict(title="Package1",details="toothpaste",weight=1,pick_up="Wein",drop_off="Lerner",author="test1",status=0), follow_redirects=True)
        assert 'Task successfully created!' in new_task.data

        # view task

        # user1 attempt to assign its own task

        # user2 chooses to run task

        # another user wants to run task same task

        # another user wants to update same task

        # user2 updates task to Complete

        # another user tries to update task to Complete & Accepted

        # user1 updates task to Complete & Accepted

        # someone tries to update status too far


    

if(__name__ == '__main__'):
    unittest.main()