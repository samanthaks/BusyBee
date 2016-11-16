from fabric.api import local


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
