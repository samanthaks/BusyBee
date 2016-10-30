from mongoengine import connect
from app.models.request import Request

connect('BusyBee')

Request.drop_collection()
task1 = Request(
    title='Task 1',
    author='sam',
    details='please pick this up',
    runner=1234,
    pick_up='db.StringField(required=True)',
    drop_off='db.StringField(required=True)',
    weight=12.4,
    status=0)
task1.save()
task2 = Request(
    title='Task 2',
    author='sam',
    details='please pick this up',
    runner=1234,
    pick_up='here',
    drop_off='there',
    weight=12.4,
    status=0)
task2.save()
