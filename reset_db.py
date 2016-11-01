from mongoengine import connect
from app.models.request_model import Request

connect('BusyBee')

Request.drop_collection()
