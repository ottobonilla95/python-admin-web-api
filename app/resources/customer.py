from flask import request
from flask_restful import Resource

# models
from models.production.customer import CustomerModel
from models.production.task import TaskModel

# schemas
from schemas.production.customer import CustomerSchema

# jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

customer_schema = CustomerSchema()

class Customer(Resource):
    @classmethod
    @jwt_required
    def get(cls, id):
        customer = CustomerModel.find_by_id (id)

        if customer:
            return customer_schema.dump(customer)

        return {"message":"not found"}, 404

    @classmethod
    @jwt_required
    def put(cls, id):

        customer_json = request.get_json()["customer"]
        customer = CustomerModel.find_by_id (id)

        if customer:
            customer.name = customer_json["name"]
            customer.mobile_number = customer_json["mobile_number"]
            customer.email = customer_json["email"]
            customer.country = customer_json["country"]
            customer.state = customer_json["state"]
            customer.street_name = customer_json["street_name"]
            customer.postal_code = customer_json["postal_code"]
            customer.latitude = customer_json["latitude"]
            customer.longitude = customer_json["longitude"]

            customer.save_to_db()

            return {"message":"customer updated", "customer": customer_schema.dump(customer)}

        return {"message":"not found"}, 404

class CustomerCreation (Resource):
    
    @classmethod
    @jwt_required
    def post (cls):

        try:
            claims = get_jwt_claims()
            company_id = claims.get("company_id")

            customer_json = request.get_json()["customer"]
            customer = customer_schema.load(customer_json)
            customer.company_id = company_id
            customer.save_to_db()

            return {"message":"customer created!", "customer":customer_schema.dump(customer)}
        except Exception as e:
            return {"message":"An error has ocurred."}, 500

class CustomerList (Resource):
    
    @classmethod
    @jwt_required
    def get (cls):

        claims = get_jwt_claims()
        company_id = claims.get("company_id")

        customers = CustomerModel.get_customers(company_id)
        return customer_schema.dump(customers, many=True)

class CustomerDeletion (Resource):
    @classmethod
    @jwt_required
    def delete(cls):
        ids = request.get_json()["ids"]
        TaskModel.delete_by_customer(ids)
        CustomerModel.delete_many(ids)
        return {"message":"customers deleted!"}

class CustomerMassiveUpload (Resource):
    @classmethod
    @jwt_required
    def post (cls):
    
        claims = get_jwt_claims()
        company_id = claims.get("company_id")

        customers_json = request.get_json()["customers"]
        customers = customer_schema.load(customers_json, many=True) 
    
        for customer in customers:
            customer.company_id = company_id

        CustomerModel.save_massive_to_db(customers)

        return {"message":"Customers added suscessfully"}

        
