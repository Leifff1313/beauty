from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
import os
import webbrowser
from threading import Timer

from model.user import UserModel
from model.TravelPlan import TravelPlanModel
from db import mongo  # Import your mongo instance
from BlockList import BlockList  # Assuming you have this module
from resources.user import blp as UserBlueprint
from resources.TravelPlan import blp as TravelPlanBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    # Configure the app with environment variables
    app.config["MONGODB_HOST"] = (
        db_url or "mongodb+srv://David:hu2177ng@cluster0.fntr2bt.mongodb.net/myDatabase"
    )
    app.config["API_TITLE"] = "Travel test API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", "your_jwt_secret_key"
    )  # Use a default value for testing

    # Initialize MongoDB
    mongo.init_app(app)

    # Initialize JWT
    jwt = JWTManager(app)

    # Define a callback function to check if the token is in the blocklist
    @jwt.token_in_blocklist_loader
    def check_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in BlockList

    # Initialize API and register blueprints
    api = Api(app)

    # Configure API with JWT authentication
    api.spec.components.security_scheme(
        "BearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    api.spec.options["security"] = [{"BearerAuth": []}]

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TravelPlanBlueprint)

    return app


def open_browser():
    webbrowser.open_new("http://localhost:5000/swagger-ui")


if __name__ == "__main__":
    app = create_app()
    # Wait for the server to start and then open the browser
    Timer(1, open_browser).start()
    app.run(debug=True)
