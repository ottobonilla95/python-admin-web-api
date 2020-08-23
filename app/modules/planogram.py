from flask import Blueprint
from flask_restful import Api

# resources
from resources.planogram import Planogram, PlanogramCreation, PlanogramList


planogram_module = Blueprint('planogram_module', __name__)
api = Api(planogram_module)

api.add_resource(Planogram, '/<string:id>')
api.add_resource(PlanogramCreation, '/create')
api.add_resource(PlanogramList, '/list')
