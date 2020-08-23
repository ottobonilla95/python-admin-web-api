from flask import Blueprint
from flask_restful import Api
from resources.auth.user import User, UserLogin, UserRegister
from resources.auth.agent import AgentLogin

auth_module = Blueprint("auth_module", __name__)

api = Api(auth_module)

api.add_resource(User, '/<string:id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(AgentLogin, '/agent/login')

