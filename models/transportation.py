from db import mongo as mg
from models.stop import StopModel
from datetime import datetime


class TransportationModel(mg.Document):
    Name = mg.StringField(required=True)
    TimeSpent = mg.IntField(required=True)
    LowCarbon = mg.BooleanField()
    CreateAt = mg.DateTimeField(default=datetime.now)
    FromStopId = mg.ReferenceField(StopModel)
    ToStopId = mg.ReferenceField(StopModel)
