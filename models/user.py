from db import mongo as mg


class UserModel(mg.Document):
    email = mg.StringField(required=True, unique=True)
    username = mg.StringField(unique=True, max_length=50)
    password = mg.StringField()
