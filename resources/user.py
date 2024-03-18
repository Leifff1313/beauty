from flask.views import MethodView
from flask_smorest import Blueprint, abort
from model.user import UserModel
from passlib.hash import pbkdf2_sha256
from db import db
from sqlalchemy.exc import SQLAlchemyError
from Schema import UserRegisterSchema, UserSchema
from BlockList import BlockList
from flask_jwt_extended import get_jwt, get_jti, create_access_token, create_refresh_token,jwt_required, get_jwt_identity
from BlockList import BlockList

blp = Blueprint("User",__name__)

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self,user_data):


        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409,message= "This user account has already been used.")


        user = UserModel(username = user_data["username"],
                         email = user_data["email"],
                         password = pbkdf2_sha256.hash(user_data["password"]))
        
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message = "error arise when item insertion to database")

        return {"Message":"the user is registered successfully"}, 201


@blp.route("/login")
class UserLogin(MethodView): 
    @blp.arguments(UserSchema) 
    def post(self,user_data):
        try:
            user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        except SQLAlchemyError:
            abort(500,message = "error arise when item insertion to database")
        if user and  pbkdf2_sha256.verify(user_data["password"],user.password):

            token = create_access_token(identity=user.id,fresh= True)
            refresh_token = create_refresh_token(identity=user.id)

            return{"access token":token,"refresh_token":refresh_token}, 201
@blp.route("/logout")        
class UserLogout(MethodView):
    @jwt_required()

    def post(self):

        jti = get_jwt()["jti"]
        
        BlockList.add(jti)
        return{"message":"logout successfully"}
    
@blp.route("/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh= True)
    def post(self):
        
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti =get_jwt()["jti"]
        BlockList.add(jti)
        # rDB.set(jti, "",ex= ACCESS_EXPIRES)
        return{"access_token": new_token}



                                  

            
