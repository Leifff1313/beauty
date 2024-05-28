from flask import Flask
from flask import Flask,jsonify
from flask_smorest import Api
from model.user import UserModel
from model.TravelPlan import TravelPlanModel
from db import mongo
import os
from resources.user import blp as UserBlueprint
from resources.TravelPlan import blp as TravelPlanBlueprint

from BlockList import BlockList
from flask_jwt_extended import JWTManager
# from flask_migrate import Migrate
from flask_mongoengine import MongoEngine

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from db import mongo  # Import your mongo instance
from BlockList import BlockList  # Assuming you have this module

def create_app(db_url=None):
    app = Flask(__name__)

    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in BlockList
    
    app.config['MONGODB_HOST'] = 'mongodb+srv://David:hu2177ng@cluster0.fntr2bt.mongodb.net/'
    app.config["API_TITLE"] = "Travel test API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    mongo.init_app(app)  # Initialize the mongo instance

    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TravelPlanBlueprint)

    
    return app
