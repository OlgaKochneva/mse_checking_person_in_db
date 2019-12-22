from mongoengine import *
from mongoengine.fields import BinaryField
from mongoengine.fields import StringField

connect(db='mse_persons')


class Persons(Document):
    name = StringField(required=True)
    face_encodings = BinaryField(required=True)
