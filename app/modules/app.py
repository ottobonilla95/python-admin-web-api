from flask import Blueprint
from flask_restful import Api

from resources.app import Menu

app_module  = Blueprint('app_module', __name__)
api = Api(app_module)

api.add_resource(Menu, '/menu')
