from flask import request
from flask_restful import Resource

# models
from models import TaskModel

# schemas
from schemas.production.task import Taskchema
from schemas.production.agent import AgentSchema

# jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

task_schema = Taskchema()
agent_schema = AgentSchema()

class Task(Resource):
    @classmethod
    def get(cls, id):
        task = TaskModel.find_by_id (id)

        if task:
            return task_schema.dump(task)

        return {"message":"not found"}, 404

    @classmethod
    def put(cls, id):

        task_json = request.get_json()["task"]
        task = TaskModel.find_by_id (id)


        if task:
            task.customer_id = task_json["customer_id"]
            task.planogram_id = task_json["planogram_id"]
            task.start_before = task_json["start_before"]
            task.complete_before = task_json["complete_before"]
            task.agent_id = task_json.get("agent_id")

            task.save_to_db()

            return {"message":"task updated", 
                    "task":
                        {
                            **task_schema.dump(task), 
                            "customer":task.customer.name,
                            "planogram":task.planogram.name,
                            "agent": task.agent.first_name if task.agent else None,
                            "agentData": agent_schema.dump(task.agent)
                        } 
            }

        return {"message":"not found"}, 404


class TaskCreation (Resource):
    @classmethod
    @jwt_required
    def post (cls):
        try:
            claims = get_jwt_claims()
            company_id = claims.get("company_id")

            task_json = request.get_json()["task"]
            task = task_schema.load(task_json)
            task.company_id = company_id

            task.save_to_db()

            return {"message":"Task created!", 
            "task":
                {
                    **task_schema.dump(task), 
                    "customer":task.customer.name,
                    "planogram":task.planogram.name,
                    "agent": task.agent.first_name if task.agent else None,
                    "agentData": agent_schema.dump(task.agent)
                } 
            }
        except Exception as e:
            return {"message":"An error has ocurred."}, 500


class TaskList (Resource):
    @classmethod
    @jwt_required
    def get (cls):

        claims = get_jwt_claims()
        company_id = claims.get("company_id")

        tasks = TaskModel.get_tasks(company_id)
        return [{
                    **task_schema.dump(task), 
                    "customer":task.customer.name,
                    "planogram":task.planogram.name,
                    "agent": task.agent.first_name if task.agent else None,
                    "agentData": agent_schema.dump(task.agent)
                    } 
                for task in tasks]

class TaskDeletion (Resource):
    @classmethod
    @jwt_required
    def delete(cls):
        ids = request.get_json()["ids"]
        TaskModel.delete_many(ids)
        return {"message":"Tasks deleted!"}


class TaskMassiveUpload (Resource):
    @classmethod
    @jwt_required
    def post (cls):
    
        claims = get_jwt_claims()
        company_id = claims.get("company_id")

       

        tasks_json = request.get_json()["tasks"]
        print(tasks_json)
        tasks = task_schema.load(tasks_json, many=True) 
    
        for task in tasks:
            task.company_id = company_id

        TaskModel.save_massive_to_db(tasks)

        return {"message":"Tasks added suscessfully"}

        
