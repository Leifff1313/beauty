from db import mongo as mg
from models.TravelPlan import TravelPlanModel


class DayModel(mg.Document):
    Date = mg.DateTimeField(required=True)
    TravelPlanId = mg.ReferenceField(TravelPlanModel)
