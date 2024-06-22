from db import mongo as mg


class PlaceModel(mg.Document):
    Name = mg.StringField(required=True)
    OpeningTime = mg.StringField()
    Address = mg.StringField()
    Long = mg.StringField()
    Lat = mg.StringField()
    Rating = mg.FloatField()
    LowCarbon = mg.BooleanField()
