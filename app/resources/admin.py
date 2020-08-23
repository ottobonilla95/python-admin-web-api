from flask_restful import Resource
from flask import request
import functools

# models
from models import UserModel

# schemas
from schemas.production.user import UserSchema
from schemas.production.user_setting import UserSettingSchema
# jwt
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity

# hashlib
from passlib.hash import pbkdf2_sha256

# constants
from constants import Roles

user_schema = UserSchema()
user_setting_schema = UserSettingSchema()
custom_pbkdf2 = pbkdf2_sha256.using(rounds=296411)


def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if user.role_id != Roles.ADMIN.value:
            return {"message":"The current user do not have the privileges to acomplish this action"}, 401

        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper



class User (Resource):
    @classmethod
    @jwt_required
    @admin_required
    def put(cls, id):
        user_json = request.get_json()["user"]

        user = UserModel.find_by_id (id)

        if user:
            if user.username != user_json.get("username") and  UserModel.find_by_username(user_json.get("username")):
                return {"message":"Username already exists"}, 400    

            if user.email != user_json.get("email") and UserModel.find_by_email(user_json.get("email")):
                return {"message":"Username already exists"}, 400
        
            user.username = user_json["username"]
            user.email = user_json["email"]
            user.role_id = user_json["role_id"]            

            if user_json["password"]:
                hashed_password = custom_pbkdf2.hash(user_json["password"])
                user.password = hashed_password

            user.save_to_db()

            return {"message":"Agent updated!", "user": user_schema.dump(user)}

        return {"message":"not found"}, 404


    @classmethod
    @jwt_required
    @admin_required
    def delete(cls, id):
        user = UserModel.find_by_id (id)

        if user:
            user.delete_from_db()

            return {"message":"User deleted!"}

        return {"message":"not found"}, 404

class UserCreationList (Resource):
    @classmethod
    @jwt_required
    @admin_required
    def post(cls):

        user_json = request.get_json()["user"]
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message":"Username already exists"}, 400    

        if UserModel.find_by_email(user.email):
            return {"message":"Username already exists"}, 400

        claims = get_jwt_claims()
        company_id = claims.get("company_id")

        user.company_id = company_id
        hashed_password = custom_pbkdf2.hash(user.password)
        user.password = hashed_password

        user.save_to_db()

        user_setting = user_setting_schema.load({"user_id":user.id})
        user_setting.save_to_db()

        return {"message":"User created!", "user": user_schema.dump(user)}


    
    @classmethod
    @jwt_required
    @admin_required
    def get(cls):
        
        claims = get_jwt_claims()
        company_id = claims.get("company_id")
        
        users = UserModel.get_users(company_id)

        return {"users":user_schema.dump(users, many=True)}

