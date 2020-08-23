from flask import Blueprint
from flask_restful import Api

from resources.compnay import Company,CompanyCreationList

company_module  = Blueprint('company_module', __name__)
api = Api(company_module)

api.add_resource(Company, '/<string:id>')
api.add_resource(CompanyCreationList, '/')

