from flask import request
from flask_restful import Resource

# models
from models.production.user import UserModel

# schemas
from schemas.production.user import UserSchema
from schemas.production.user_setting import UserSettingSchema

# hashlib
from passlib.hash import pbkdf2_sha256

# jwt
from flask_jwt_extended import create_access_token, create_refresh_token

user_schema = UserSchema()
user_setting_schema = UserSettingSchema()

custom_pbkdf2 = pbkdf2_sha256.using(rounds=296411)


class User (Resource):
    @classmethod
    def delete (cls, id):
        user = UserModel.find_by_id(id)

        if user:
            user.delete_from_db()
            return {"message":"user deleted"}
        
        return {"message":"not found"}, 404


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()["user"]

        user = user_schema.load(user_json)
        
        if UserModel.find_by_username(user.username):
            return {"message":"Username already exists"}, 400    

        if UserModel.find_by_email(user.email):
            return {"message":"Username already exists"}, 400

        hashed_password = custom_pbkdf2.hash(user.password)
        user.password = hashed_password

        user.save_to_db()

        user_setting = user_setting_schema.load({"user_id":user.id})
        user_setting.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True, expires_delta=False,user_claims={"company_id":user.company_id, "role":user.role_id})
        refresh_token = create_refresh_token(user.id)

        return {
            "message":"User Logged In",
            "user":{ 
                "user": {
                    user_schema.dump(user),
                    *{"profile_config":user_setting_schema.dump(user_setting)}

                } ,
                "userToken":{
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                }
            },
        }

class UserLogin (Resource):
    @classmethod
    def post(cls):
        
        email_username = request.get_json()["email_username"]
        password = request.get_json()["password"]

        userFound = UserModel.find_by_username_or_email(email_username, email_username)

        if userFound and custom_pbkdf2.verify(password, userFound.password):
            
            access_token = create_access_token(identity=userFound.id, fresh=True, expires_delta=False, user_claims={"company_id":userFound.company_id, "role":userFound.role_id})
            refresh_token = create_refresh_token(userFound.id)

            return {
                "message":"User Logged In",
                "user":{ 
                    "user": {
                        **user_schema.dump(userFound),
                        **{"profile_config":user_setting_schema.dump(userFound.profile_config)}
                    } ,
                    "userToken":{
                        "access_token":access_token,
                        "refresh_token":refresh_token,
                    }
                },
            }

        return {"message":"Invalid credentials"}, 400