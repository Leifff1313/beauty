from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only= True)

class UserRegisterSchema(UserSchema):
     email = fields.Str(required=True)

class AddTravelPlanSchema(Schema):
    email = fields.Str(required=True)
    planname = fields.Str(required=True)
    startdate = fields.Str(required=True)
    enddate = fields.Str(required=True)