from flask.views import MethodView
from flask_smorest import Blueprint, abort
from model.user import UserModel
from model.TravelPlan import TravelPlanModel

from passlib.hash import pbkdf2_sha256
from db import mongo
from Schema import UserRegisterSchema, UserSchema, AddTravelPlanSchema
from BlockList import BlockList
from flask_jwt_extended import (
    get_jwt,
    get_jti,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from BlockList import BlockList
from flask import jsonify
from datetime import datetime


blp = Blueprint("TravelPlan", __name__)


@blp.route("/travelPlan")
class TravelPlan(MethodView):
    @blp.arguments(AddTravelPlanSchema)
    def post(self, user_data):
        try:
            user = UserModel.objects(email=user_data["email"]).first()
        except Exception as e:
            abort(
                500,
                description=f"An error occurred when querying the database: {str(e)}",
            )

        if user:
            travelplan = TravelPlanModel(
                planname=user_data["planname"],
                startdate=user_data["startdate"],
                enddate=user_data["enddate"],
                createAt=datetime.now(),
                user=user,
            )
            travelplan.save()
            return {
                "message": f'{user.username} created a travelplan named {user_data["planname"]}'
            }

        return {"message": "adding unsuccessfully"}

    @jwt_required()
    def get(self):
        user_email = get_jwt_identity()
        print(user_email)
        try:
            user = UserModel.objects(email=user_email).first()
        except Exception as e:
            abort(
                500,
                description=f"An error occurred when querying the database: {str(e)}",
            )

        if user:
            try:
                travelplans = TravelPlanModel.objects(user=user)
            except Exception as e:
                abort(
                    500,
                    description=f"An error occurred when querying the database: {str(e)}",
                )

            travelplans_list = []
            for plan in travelplans:
                travelplans_list.append(
                    {
                        "planname": plan.planname,
                        "startdate": plan.startdate,
                        "enddate": plan.enddate,
                        "createdAt": plan.createAt,
                    }
                )

            return jsonify(travelplans_list)

        return {"message": "User not found"}, 404
