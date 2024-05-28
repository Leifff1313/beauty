from flask.views import MethodView
from flask_smorest import Blueprint, abort
from model.user import UserModel
from model.TravelPlan import TravelPlanModel

from passlib.hash import pbkdf2_sha256
from db import mongo
from Schema import UserRegisterSchema, UserSchema, AddTravelPlanSchema
from BlockList import BlockList
from flask_jwt_extended import get_jwt, get_jti, create_access_token, create_refresh_token,jwt_required, get_jwt_identity
from BlockList import BlockList
from flask import jsonify
from datetime import datetime


blp = Blueprint("TravelPlan",__name__)



@blp.route("/addPlan")
class AddTravelPlan(MethodView):
    @blp.arguments(AddTravelPlanSchema)
    def post(self,user_data):

        try:
            
            user = UserModel.objects(email=user_data["email"]).first()
        except Exception as e:
            abort(500, description=f"An error occurred when querying the database: {str(e)}")
        if user:
            travelplan = TravelPlanModel(planname = user_data['planname'],startdate = user_data['startdate'],enddate = user_data['enddate'],createAt = datetime.now(), user = user)
            travelplan.save()

            
            return {"message": f'{user.username} create a travelplan named {user_data['planname']}'}
        return {"message": "adding unsuccessfully"}