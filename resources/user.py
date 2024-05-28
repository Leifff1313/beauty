from flask.views import MethodView
from flask_smorest import Blueprint, abort
from model.user import UserModel
from passlib.hash import pbkdf2_sha256
from db import mongo
from Schema import UserRegisterSchema, UserSchema
from BlockList import BlockList
from flask_jwt_extended import get_jwt, get_jti, create_access_token, create_refresh_token,jwt_required, get_jwt_identity
from BlockList import BlockList
from flask import jsonify

blp = Blueprint("User",__name__)
    

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self,user_data):

        # print('ok')
        if UserModel.objects(username=user_data["username"]).first():
            abort(409, description="This user account has already been used.")



        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        
        try:
            user.save()
        except  Exception as e:
                abort(500, description=f"Error arise when inserting item to database: {str(e)}")


        return {"Message":"the user is registered successfully"}, 201


@blp.route("/login")
class UserLogin(MethodView): 
    @blp.arguments(UserSchema) 
    def post(self,user_data):
        try:
            user = UserModel.objects(username=user_data["username"]).first()
        except Exception as e:
            # print('error')
            abort(500, description=f"An error occurred when querying the database: {str(e)}")
        if user and  pbkdf2_sha256.verify(user_data["password"], user.password):

            token = create_access_token(identity=str(user.id),fresh= True)
            refresh_token = create_refresh_token(identity=str(user.id))

            return{"access_token":token,"refresh_token":refresh_token}, 201
        else:
            abort(401, description="Invalid credentials")
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



                                  

            
