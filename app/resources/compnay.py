from flask_restful import Resource
from flask import request
import functools

# models
from models import CompanyModel, UserModel

# schemas
from schemas.production.compnay import CompanySchema
from schemas.production.user import UserSchema
from schemas.production.user_setting import UserSettingSchema

# jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

# constants
from constants import Roles

# hashlib
from passlib.hash import pbkdf2_sha256

custom_pbkdf2 = pbkdf2_sha256.using(rounds=296411)
company_schema = CompanySchema()
user_schema = UserSchema()
user_setting_schema = UserSettingSchema()

def super_admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if user.role_id != Roles.SUPER_ADMIN.value:
            return {"message":"The current user do not have the privileges to acomplish this action"}, 401

        return func(*args, **kwargs)
    return wrapper


class Company (Resource):
    @classmethod
    @jwt_required
    @super_admin_required
    def get(cls, id):
    
        company = CompanyModel.find_by_id (id)

        if company:
            return {"company":company_schema.dump(company)}

        return {"message":"not found"}, 404


    @classmethod
    @jwt_required
    @super_admin_required
    def put(cls, id):
  
        company_json = request.get_json()["company"]
        users_json = company_json["users"]
        company = CompanyModel.find_by_id(id)

        if company:

            # validate company
            if company_json.get("name") != company.name or company_json.get("email") != company.email:
                if CompanyModel.find_by_name_or_email(company_json.get("name"),company_json.get("email")):
                    return {"message":"Company name or email already exists"}, 400


            # delete users
            new_users = []
            for user in company.users:               
                exists_user = next(filter(lambda usr: usr.get("id") == user.id, users_json), None)

                if exists_user:
                    new_users.append(user)
            
            company.users = new_users

            # validates usernames and emails
            for new_user in users_json:
          
                current_user = next(filter(lambda usr: usr.id and usr.id == new_user.get("id"), company.users), None)
                
                # if the user already exists
                if current_user:
      
                    if current_user.username != new_user.get("username") :
                        if UserModel.find_by_username(new_user.get("username")):
                            return {"message":"Username or email already exists11"}, 400
                          
                    if current_user.email != new_user.get("email"):
                        if UserModel.find_by_email(new_user.get("email")):
                            return {"message":"Username or email already exists11"}, 400

                    current_user.username = new_user["username"]
                    current_user.email = new_user["email"]
                    current_user.role_id = new_user["role_id"]        
                    
                    if new_user.get("password"):
                        hashed_password = custom_pbkdf2.hash(new_user.get("password"))
                        current_user.password = hashed_password

                # if the user is new
                else:

                    if UserModel.find_by_username_or_email(new_user.get("username"),new_user.get("email")):
                        return {"message":"Username or email already exists22"}, 400

                    hashed_password = custom_pbkdf2.hash(new_user["password"])
                    new_user["password"] = hashed_password

                    user_to_add = user_schema.load(new_user)
                    company.users.append(user_to_add)

            
            company.name = company_json.get("name")
            company.email = company_json.get("email")
            company.mobile_number = company_json.get("mobile_number")
            company.address = company_json.get("address")

            company.save_to_db()

            for user in company.users:
                if not user.profile_config:
                    user_setting = user_setting_schema.load({"user_id":user.id})
                    user_setting.save_to_db()

            return {"message":"Company updated", "company":company_schema.dump(company)}

        return {"message":"not found"}, 404


    @classmethod
    @jwt_required
    @super_admin_required
    def delete(cls, id):
        
        company = CompanyModel.find_by_id (id)

        if company:
            company.delete_from_db()

            return {"message":"Compnay deleted!"}

        return {"message":"not found"}, 404

class CompanyCreationList (Resource):
    @classmethod
    @jwt_required
    @super_admin_required
    def post(cls):
        try:
         
            company_json = request.get_json()["company"]
            company = company_schema.load(company_json)

            for user in company.users:
                if UserModel.find_by_username(user.username):
                    return {"message":"Username already exists"}, 400    

                if UserModel.find_by_email(user.email):
                    return {"message":"Username already exists"}, 400

                hashed_password = custom_pbkdf2.hash(user.password)
                user.password = hashed_password
            
            company.save_to_db()

            for user in company.users:
                user_setting = user_setting_schema.load({"user_id":user.id})
                user_setting.save_to_db()

            return {"message":"Company created!", "company":company_schema.dump(company)}

        except Exception as e:
            return {"message":"An error has occurred!"}
            
    @classmethod
    @jwt_required
    @super_admin_required
    def get(cls):
   
        companies = CompanyModel.get_companies()

        return {"companies":company_schema.dump(companies, many=True)}


