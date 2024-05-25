from db import mongo

class UserModel(mongo.Document):
    email = mongo.StringField(required=True, unique=True)
    username = mongo.StringField(max_length=50)
    password = mongo.StringField()
