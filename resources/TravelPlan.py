from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.user import UserModel
from models.travelPlan import TravelPlanModel

from db import mongo
from Schema import UserSchema, AddTravelPlanSchema, UpdateTravelPlanSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from datetime import datetime

blp = Blueprint("TravelPlan", __name__, url_prefix="/travel_plans")


@blp.route("/")
class TravelPlanList(MethodView):

    @blp.arguments(AddTravelPlanSchema)
    @jwt_required()
    def post(self, travel_plan_data):
        user_id = get_jwt_identity()
        user = UserModel.objects(id=user_id).first()
        if not user:
            abort(404, description="User not found")

        travel_plan = TravelPlanModel(
            planname=travel_plan_data["planname"],
            startdate=travel_plan_data["startdate"],
            enddate=travel_plan_data["enddate"],
            createAt=datetime.now(),
            user=user,
        )
        travel_plan.save()
        return {
            "message": f'{user.username} created a travel plan named {travel_plan_data["planname"]}'
        }, 201

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.objects(id=user_id).first()
        if not user:
            abort(404, description="User not found")

        travel_plans = TravelPlanModel.objects(user=user)
        return jsonify(
            [
                {
                    "planname": plan.planname,
                    "startdate": plan.startdate,
                    "enddate": plan.enddate,
                    "createdAt": plan.createAt,
                }
                for plan in travel_plans
            ]
        )


@blp.route("/<string:plan_id>")
class TravelPlanItem(MethodView):

    @jwt_required()
    def get(self, plan_id):
        user_id = get_jwt_identity()
        travel_plan = TravelPlanModel.objects(id=plan_id, user=user_id).first()
        if not travel_plan:
            abort(404, description="Travel plan not found")
        return {
            "planname": travel_plan.planname,
            "startdate": travel_plan.startdate,
            "enddate": travel_plan.enddate,
            "createdAt": travel_plan.createAt,
        }

    @blp.arguments(UpdateTravelPlanSchema)
    @jwt_required()
    def put(self, update_data, plan_id):
        user_id = get_jwt_identity()
        TravelPlanModel.objects(id=plan_id, user=user_id).update(**update_data)
        return {"message": "Travel plan updated successfully"}

    @jwt_required()
    def delete(self, plan_id):
        user_id = get_jwt_identity()
        travel_plan = TravelPlanModel.objects(id=plan_id, user=user_id).first()
        if not travel_plan:
            abort(404, description="Travel plan not found")
        travel_plan.delete()
        return {"message": "Travel plan deleted successfully"}
