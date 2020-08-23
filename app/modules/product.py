from flask import Blueprint
from flask_restful import Api

# resources
from resources.product import Product, ProductCreation, ProductDeletion, ProductList, ProductMassiveUpload


product_module = Blueprint('product_module', __name__)
api = Api(product_module)

api.add_resource(Product, '/<string:id>')
api.add_resource(ProductCreation, '/create')
api.add_resource(ProductDeletion, '/delete')
api.add_resource(ProductList, '/list')
api.add_resource(ProductMassiveUpload, '/massive')

