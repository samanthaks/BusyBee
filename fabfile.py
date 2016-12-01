from fabric.api import local, env


def first_setup():
    local("pip install virtualenv")
    local("virtualenv .")
    local("source bin/activate")
    local("pip install -r requirements.txt")
    local("deactivate")


def run_local():
    local("python run.py")


def update_req():
    local("pip freeze > requirements.txt")


def enter_venv():
    local("source bin/activate")


def run_tests():
    local("python -m unittest tests")


def run_SA():
    env.warn_only = True
    user_route_test()
    task_route_test()
    home_route_test()
    user_model_test()
    task_model_test()
    init_test()
    unittest_test()


def user_route_test():
    local("pylint app/routes/user_route.py")


def task_route_test():
    local("pylint app/routes/task_route.py")


def home_route_test():
    local("pylint app/routes/home_route.py")


def user_model_test():
    local("pylint app/models/user_model.py")


def task_model_test():
    local("pylint app/models/task_model.py")


def init_test():
    local("pylint app/__init__.py")


def unittest_test():
    local("pylint tests.py")
