from db import mongo as mg


class StopModel(mg.Document):
    Name = mg.StringField(required=True)
    StartTime = mg.DateTimeField()
    EndTime = mg.DateTimeField()
    note = mg.StringField()
    PlaceId = mg.ReferenceField("PlaceModel")
    DayId = mg.ReferenceField("DayModel")
