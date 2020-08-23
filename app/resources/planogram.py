from flask import request
from flask_restful import Resource

# models
from models import PlanogramModel, TaskModel

# schemas
from schemas.production.planogram import PlanogramSchema

# jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

# libs
from libs.cdmanager import CloudinaryHandler
from libs.utils import Utils

planogram_schema = PlanogramSchema()

class Planogram(Resource):
    @classmethod
    @jwt_required
    def get(cls, id):
        planogram = PlanogramModel.find_by_id (id)

        if planogram:
            return planogram_schema.dump(planogram)

        return {"message":"not found"}, 404

    @classmethod
    @jwt_required
    def put(cls, id):

        planogram_json = request.get_json()["planogram"]
        planogram = PlanogramModel.find_by_id (id)

        if planogram:
            planogram.name = planogram_json["name"]
            planogram.description = planogram_json["description"]
            planogram.version = planogram_json["version"]

            if planogram_json.get("image"):
        
                
                if planogram_json.get("image") == "NOIMAGE":
                    planogram.image = None

                else:
                    name = planogram_json.get("name")
                    final_url = CloudinaryHandler.LoadImage(planogram_json.get("image"))
                    planogram.image = final_url

            planogram.save_to_db()

            return {"message":"planogram updated", "planogram": planogram_schema.dump(planogram)}

        return {"message":"not found"}, 404

    @classmethod
    def delete(cls, id):

        task = TaskModel.find_by_planogram(id)
        
        if task:
            return {"message":"There are task with this planogram"}, 400

        planogram = PlanogramModel.find_by_id (id)

        if planogram:
            planogram.delete_from_db()
            

            return {"message":"Planogram deleted!"}

        return {"message":"not found"}, 404


class PlanogramCreation (Resource):
    @classmethod
    @jwt_required
    def post (cls):
        try:
            claims = get_jwt_claims()
            company_id = claims.get("company_id")
            
            planogram_json = request.get_json()["planogram"]  

            if planogram_json.get("image"):
                name = planogram_json.get("name")
                final_url = CloudinaryHandler.LoadImage(planogram_json.get("image"))
                
                planogram_json["image"] = final_url


            planogram = planogram_schema.load(planogram_json)
            planogram.company_id = company_id

            planogram.save_to_db()

            return {"message":"Planogram created!", "planogram":planogram_schema.dump(planogram)}
        except Exception as e:
            return {"message":"An error has ocurred."}, 500


class PlanogramList (Resource):
    @classmethod
    @jwt_required
    def get (cls):

        claims = get_jwt_claims()
        company_id = claims.get("company_id")

        planograms = PlanogramModel.get_planograms(company_id)
        return planogram_schema.dump(planograms, many=True)
