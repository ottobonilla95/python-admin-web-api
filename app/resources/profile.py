from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

# models
from models import UserModel, UserSettingModel

# schemas
from schemas.production.user import UserSchema
from schemas.production.user_setting import UserSettingSchema

user_schema = UserSchema()
user_setting_schema = UserSettingSchema ()

class UserProfile (Resource):
    @classmethod
    @jwt_required
    def put(cls):
        user_id = get_jwt_identity()
        user_json = request.get_json()["userProfile"]
        user = UserModel.find_by_id(user_id)

        user.username = user_json.get("username")

        user.save_to_db()

        return {"message":"User profile updated!", "user":user_schema.dump(user)}


class UserEmail (Resource):
    @classmethod
    @jwt_required
    def put(cls):
        user_id = get_jwt_identity()

        email = request.get_json()["email"]
        
        if UserModel.find_by_email(email):
            return {"message":"Username already exists"}, 400

        user = UserModel.find_by_id(user_id)

        user.email = email

        user.save_to_db()

        return {"message":"Email updated!", "user":user_schema.dump(user)}

class UserLanguage (Resource):
    @classmethod
    @jwt_required
    def put(cls):
        user_id = get_jwt_identity()

        language = request.get_json()["language"]
        user_settings = UserSettingModel.find_by_user_id(user_id)

        user_settings.language = language

        user_settings.save_to_db()

        return {
                "message":"Language preferences updated!", 
                "profile_config":user_setting_schema.dump(user_settings)
                }

class UserTheme (Resource):
    @classmethod
    @jwt_required
    def put(cls):
        user_id = get_jwt_identity()

        profile_settings = request.get_json()["profile_settings"]
        user_settings = UserSettingModel.find_by_user_id(user_id)

        user_settings.active_theme = profile_settings.get("activeTheme")
        user_settings.is_dark_sidenav = profile_settings.get("isDarkSidenav")
        user_settings.enable_sidebar_background_image = profile_settings.get("enableSidebarBackgroundImage")
        user_settings.selected_sidebar_image = profile_settings.get("selectedSidebarImage")
        user_settings.mini_sidebar = profile_settings.get("miniSidebar")
        user_settings.box_layout = profile_settings.get("boxLayout")
        user_settings.rtl_layout = profile_settings.get("rtlLayout")
        user_settings.dark_mode = profile_settings.get("darkMode")

        user_settings.save_to_db()


        return {
                "message":"Theme preferences updated!", 
                "profile_config":user_setting_schema.dump(user_settings)
                }