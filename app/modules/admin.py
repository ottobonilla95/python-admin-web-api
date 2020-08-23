from flask import Blueprint
from flask_restful import Api

from resources.admin import User,UserCreationList

admin_module  = Blueprint('admin_module', __name__)
api = Api(admin_module)

api.add_resource(User, '/user/<string:id>')
api.add_resource(UserCreationList, '/user')

