from flask import request
from flask_restful import Resource

# models
from models.production.product import ProductModel

# schemas
from schemas.production.product import ProductSchema

# jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

# libs
from libs.cdmanager import CloudinaryHandler
from libs.utils import Utils

product_schema = ProductSchema()

class Product(Resource):
    @classmethod
    def get(cls, id):
        product = ProductModel.find_by_id (id)

        if product:
            return product_schema.dump(product)

        return {"message":"not found"}, 404

    @classmethod
    def put(cls, id):

        product_json = request.get_json()["product"]
        product = ProductModel.find_by_id (id)

        if product:
            product.name = product_json["name"]
            product.upc = product_json["upc"]
            product.category = product_json["category"]
            product.sub_category = product_json["sub_category"]
            product.brand = product_json["brand"]
            product.sub_brand = product_json["sub_brand"]
            product.container = product_json["container"]
            product.volume = product_json["volume"]
            product.width_size = product_json["width_size"]
            product.height_size = product_json["height_size"]

            if product_json.get("image"):
                
                if product_json.get("image") == "NOIMAGE":
                    product.image = None

                else:
                    name = product_json.get("name")
                    final_url = CloudinaryHandler.LoadImage(product_json.get("image"))
                    product.image = final_url


            product.save_to_db()

            return {"message":"product updated", "product": product_schema.dump(product)}

        return {"message":"not found"}, 404


class ProductCreation (Resource):
    @classmethod
    @jwt_required
    def post (cls):
        try:
            claims = get_jwt_claims()
            company_id = claims.get("company_id")

            product_json = request.get_json()["product"]

            if product_json.get("image"):
                name = product_json.get("name")
                final_url = CloudinaryHandler.LoadImage(product_json.get("image"))

                product_json["image"] = final_url

            product = product_schema.load(product_json)
            product.company_id = company_id

            product.save_to_db()

            return {"message":"Product created!", "product":product_schema.dump(product)}
        except Exception as e:
            return {"message":"An error has ocurred."}, 500


class ProductList (Resource):
    @classmethod
    @jwt_required
    def get (cls):

        claims = get_jwt_claims()
        company_id = claims.get("company_id")

        products = ProductModel.get_products(company_id)
        return product_schema.dump(products, many=True)

class ProductDeletion (Resource):
    @classmethod
    @jwt_required
    def delete(cls):
        ids = request.get_json()["ids"]

        products = ProductModel.get_many(ids)

        ProductModel.delete_many(ids)

        return {"message":"Products deleted!"}

class ProductMassiveUpload (Resource):
    @classmethod
    @jwt_required
    def post (cls):
    
        claims = get_jwt_claims()
        company_id = claims.get("company_id")

        products_json = request.get_json()["products"]
        products = product_schema.load(products_json, many=True) 
    
        for product in products:
            product.company_id = company_id

        ProductModel.save_massive_to_db(products)

        return {"message":"Products added suscessfully"}

        
