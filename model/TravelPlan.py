from db import mongo as mg
from datetime import datetime
from .user import UserModel


class TravelPlanModel(mg.Document):
    planname = mg.StringField(required=True)
    startdate = mg.StringField()
    enddate = mg.StringField()
    createAt = mg.DateTimeField(default=datetime.now())
    user = mg.ReferenceField(document_type=UserModel)



