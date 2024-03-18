from flask import Flask
from flask import Flask,jsonify
from flask_smorest import Api
from model.user import UserModel
from db import db
import os
from resources.user import blp as UserBlueprint
from BlockList import BlockList
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

def create_app(db_url = None):
   
    app = Flask(__name__)

    jwt = JWTManager(app)
    @jwt.token_in_blocklist_loader
    def check_token_in_blocklist(jwt_header,jwt_payload):
        jti = jwt_payload["jti"]
       
        return jti  in BlockList


    app.config["API_TITLE"] = " Travel test API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_SECRET_KEY"] ="127605168684557772074256969153596259963"
    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)
    api.register_blueprint(UserBlueprint)

    return app

    
