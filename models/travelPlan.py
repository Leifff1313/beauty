from db import mongo as mg
from datetime import datetime
from models.user import UserModel


class TravelPlanModel(mg.Document):
    planname = mg.StringField(required=True)
    startdate = mg.DateTimeField(required=True)
    enddate = mg.DateTimeField(required=True)
    createAt = mg.DateTimeField(default=datetime.now())
    user = mg.ReferenceField(document_type=UserModel)
