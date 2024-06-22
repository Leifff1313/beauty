from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)


class AddTravelPlanSchema(Schema):
    planname = fields.Str(required=True, validate=validate.Length(min=1))
    startdate = fields.DateTime(required=True)
    enddate = fields.DateTime(required=True)
    # `user` 字段在這裡不需要，因為 `user` 是從 JWT token 獲取的


class UpdateTravelPlanSchema(Schema):
    planname = fields.Str(validate=validate.Length(min=1))
    startdate = fields.DateTime()
    enddate = fields.DateTime()
    id = fields.Str(dump_only=True)  # 只在序列化時包括
    Name = fields.Str(required=True, validate=validate.Length(min=1))
    StartDay = fields.DateTime(required=True)
    EndDay = fields.DateTime(required=True)
    CreateAt = fields.DateTime(dump_only=True)
    UserId = fields.Str(required=True, load_only=True)  # 只在加載時包括
