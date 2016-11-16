from app import create_app as create_app_base
from app.models.task_model import Request
from mongoengine import connect
import unittest
from flask_testing import TestCase


class Test_Class(TestCase):

    def create_app(self):
        return create_app_base(
            MONGO={'db': 'test_db'},
            TESTING=True,
            CSRF_ENABLED=False,
            WTF_CSRF_ENABLED=False
        )

    def setUp(self):
        self.app = self.create_app()

    def tearDown(self):
        database = connect()
        database.drop_database('test_db')

    def test_non_user_pages(self):
        render_templates = False
        #check pages where user is not logged in 
        index_page = self.client.get('/')
        assert 'Welcome to BusyBee' in index_page.data

        login_page = self.client.get('/login')
        assert 'Username' in login_page.data
        assert 'Password' in login_page.data
        assert 'Sign In' in login_page.data
        assert 'Sign Up' in login_page.data

        signup_page = self.client.get('/signup')
        assert 'Username' in signup_page.data
        assert 'Password' in signup_page.data
        assert 'Email' in signup_page.data
        assert 'Submit' in signup_page.data

    def test_user(self):
        # Check valid credentials
        valid_signup = self.client.post('/signup', data=dict(Email='test1@test.com', Username='test1', Password='password'), follow_redirects=True)
        assert 'Thanks for registering. Please Log In' in valid_signup.data

        # Duplicate Email
        invalid_signup = self.client.post('/signup', data=dict(Email='test1@test.com', Username='test2', Password='password'), follow_redirects=True)
        assert 'Email already exists, choose another!' in invalid_signup.data

        # Duplicate Username
        invalid_signup = self.client.post('/signup', data=dict(Email='test2@test.com', Username='test1', Password='password'), follow_redirects=True)
        assert 'Username already exists, choose another!' in invalid_signup.data

        # invalid login - username
        invalid_login = self.client.post('/login', data=dict(Username='test123', Password='password2'), follow_redirects=True)
        assert 'User does not exist. Please Sign Up' in invalid_login.data

        # invalid login - password
        invalid_login = self.client.post('/login', data=dict(Username='test1', Password='password2'), follow_redirects=True)
        assert 'Wrong password!' in invalid_login.data

        # valid login
        valid_login = self.client.post('/login', data=dict(Username='test1', Password='password'), follow_redirects=True)
        assert 'Logged in successfully!' in valid_login.data

        # Test log out
        logout = self.client.get('logout', follow_redirects=True)
        assert 'You were logged out!' in logout.data


    def test_tasks(self):
        # views w/o login
        invalid_view = self.client.get('/tasks', follow_redirects=True)
        assert 'You need to be logged in to access this page' in invalid_view.data

        invalid_view = self.client.get('/new_task', follow_redirects=True)
        assert 'You need to be logged in to access this page' in invalid_view.data

        invalid_view = self.client.get('/view', follow_redirects=True)
        assert 'You need to be logged in to access this page' in invalid_view.data

        # valid login
        valid_signup = self.client.post('/signup', data=dict(Email='test1@test.com', Username='test1', Password='password'), follow_redirects=True)
        valid_login = self.client.post('/login', data=dict(Username='test1', Password='password'), follow_redirects=True)
        assert 'Logged in successfully!' in valid_login.data

        # views w/ login
        valid_view = self.client.get('/tasks', follow_redirects=True)
        assert 'All Tasks' in valid_view.data

        valid_view = self.client.get('/new_task', follow_redirects=True)
        assert 'Post A New Request' in valid_view.data
        assert 'title' in valid_view.data
        assert 'details' in valid_view.data
        assert 'weight' in valid_view.data
        assert 'pick_up' in valid_view.data
        assert 'drop_off' in valid_view.data

        valid_view = self.client.get('/view', follow_redirects=True)
        assert 'Page Not Found' in valid_view.data

        # Test posting task
        new_task = self.client.post('/new_task', data=dict(title="Package1",details="toothpaste",weight=1,pick_up="Wein",drop_off="Lerner",author="test1",status=0), follow_redirects=True)
        assert 'Task successfully created!' in new_task.data

        # view task invalid
        invalid_view = self.client.get('/view?id=12345', follow_redirects=True)
        assert 'Page Not Found' in invalid_view.data

        # view task valid
        database = connect()
        task = Request.objects.get(author="test1")
        valid_view = self.client.get('/view?id='+str(task.id), follow_redirects=True)
        assert 'New' in valid_view.data
        assert 'Back to Tasks' in valid_view.data

        # user1 attempt to assign its own task
        invalid_request = self.client.get('/view?status=0&id='+str(task.id), follow_redirects=True)
        assert 'You cannot assign yourself your own task' in invalid_request.data
        task = Request.objects.get(author="test1")
        self.assertEqual(task.status,0)

        # user2 chooses to run task
        self.client.post('/logout', follow_redirects=True)
        self.client.post('/signup', data=dict(Email='test2@test.com', Username='test2', Password='password'), follow_redirects=True)
        self.client.post('/login', data=dict(Username='test2', Password='password'), follow_redirects=True)
        valid_task_run = self.client.get('/view?status=0&id='+str(task.id), follow_redirects=True)
        task = Request.objects.get(author="test1")
        assert 'Task Status Updated: Assigned to test2' in valid_task_run.data
        self.assertEqual(task.status,1)

        # another user wants to run task same task
        self.client.post('/logout', follow_redirects=True)
        self.client.post('/signup', data=dict(Email='test3@test.com', Username='test3', Password='password'), follow_redirects=True)
        self.client.post('/login', data=dict(Username='test3', Password='password'), follow_redirects=True)
        valid_task_run = self.client.get('/view?status=0&id='+str(task.id), follow_redirects=True)
        assert 'This task has already been assigned' in valid_task_run.data

        # another user wants to update same task
        valid_task_run = self.client.get('/view?status=1&id='+str(task.id), follow_redirects=True)
        assert 'You cannot update a task someone else is doing' in valid_task_run.data

        # user2 updates task to Complete
        self.client.post('/logout', follow_redirects=True)
        self.client.post('/login', data=dict(Username='test2', Password='password'), follow_redirects=True)
        valid_task_run = self.client.get('/view?status=1&id='+str(task.id), follow_redirects=True)
        assert 'Task Status Updated: Completed' in valid_task_run.data

        # another user tries to update task to Complete & Accepted
        self.client.post('/logout', follow_redirects=True)
        self.client.post('/login', data=dict(Username='test3', Password='password'), follow_redirects=True)
        valid_task_run = self.client.get('/view?status=2&id='+str(task.id), follow_redirects=True)
        assert 'Only the Task Author can mark this task' in valid_task_run.data

        # user1 updates task to Complete & Accepted
        self.client.post('/logout', follow_redirects=True)
        self.client.post('/login', data=dict(Username='test1', Password='password'), follow_redirects=True)
        valid_task_run = self.client.get('/view?status=2&id='+str(task.id), follow_redirects=True)
        assert 'Task Status Updated: Completed &amp; Accepted' in valid_task_run.data

        # user1 tries to update status after Complete & Accepted
        valid_task_run = self.client.get('/view?status=2&id='+str(task.id), follow_redirects=True)
        assert 'You have already marked this task Completed &amp; Accepted' in valid_task_run.data

        # a user tries to a different status number
        valid_task_run = self.client.get('/view?status=5&id='+str(task.id), follow_redirects=True)
        assert 'Page Not Found' in valid_task_run.data


if(__name__ == '__main__'):
    unittest.main()