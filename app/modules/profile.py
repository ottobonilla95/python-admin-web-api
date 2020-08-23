from flask import Blueprint
from flask_restful import Api
from resources.profile import UserProfile, UserEmail, UserLanguage, UserTheme

profile_module = Blueprint("profile_module", __name__)

api = Api(profile_module)

api.add_resource(UserProfile, '/')
api.add_resource(UserEmail, '/email')
api.add_resource(UserLanguage, '/language')
api.add_resource(UserTheme, '/theme')