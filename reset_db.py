from mongoengine import connect
from app.models.task_model import Request
from app.models.user_model import User

database = connect()
database.drop_database('BusyBee')
