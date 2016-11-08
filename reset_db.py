from mongoengine import connect
from app.models.task_model import Request
from app.models.user_model import User

connect('BusyBee')

Request.drop_collection()
User.drop_collection()