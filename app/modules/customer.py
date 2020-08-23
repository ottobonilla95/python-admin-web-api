from flask import Blueprint
from flask_restful import Api

# resources
from resources.customer import Customer, CustomerCreation, CustomerList, CustomerDeletion,CustomerMassiveUpload


customer_module = Blueprint('customer_module', __name__)
api = Api(customer_module)

api.add_resource(Customer, '/<string:id>')
api.add_resource(CustomerCreation, '/create')
api.add_resource(CustomerDeletion, '/delete')
api.add_resource(CustomerList, '/list')
api.add_resource(CustomerMassiveUpload, '/massive')





