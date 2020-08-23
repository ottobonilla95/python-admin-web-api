from flask import request
from flask_restful import Resource

# models
from models import AgentModel, TaskModel

# schemas
from schemas.production.agent import AgentSchema

# jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

# hashlib
from passlib.hash import pbkdf2_sha256

# libs
from libs.cdmanager import CloudinaryHandler
from libs.utils import Utils


agent_schema = AgentSchema()
custom_pbkdf2 = pbkdf2_sha256.using(rounds=296411)

class Agent(Resource):
    @classmethod
    @jwt_required
    def get(cls, id):
        agent = AgentModel.find_by_id (id)

        if agent:
            return agent_schema.dump(agent)

        return {"message":"not found"}, 404

    @classmethod
    @jwt_required
    def put(cls, id):

        agent_json = request.get_json()["agent"]
        agent = AgentModel.find_by_id (id)

        if agent:
            agent.first_name = agent_json["first_name"]
            agent.last_name = agent_json["last_name"]
            agent.username = agent_json["username"]            
            agent.email = agent_json["email"]
            agent.mobile_number = agent_json["mobile_number"]
            agent.country = agent_json["country"]

            if agent_json["password"]:
                hashed_password = custom_pbkdf2.hash(agent_json["password"])
                agent.password = hashed_password

            if agent_json.get("image"):
                
                             
                if agent_json.get("image") == "NOIMAGE":
                    agent.image = None

                else:
                    first_name = agent_json.get("first_name")
                    final_url = CloudinaryHandler.LoadImage(agent_json.get("image"))
                    agent.image = final_url

            agent.save_to_db()

            return {"message":"Agent updated!", "agent": agent_schema.dump(agent)}

        return {"message":"not found"}, 404


class AgentCreation (Resource):
    @classmethod
    @jwt_required
    def post (cls):
        try:
            claims = get_jwt_claims()
            company_id = claims.get("company_id")

            agent_json = request.get_json()["agent"]
            
            if agent_json.get("image"):
                first_name = agent_json.get("first_name")
                final_url = CloudinaryHandler.LoadImage(agent_json.get("image"))

                agent_json["image"] = final_url

            agent = agent_schema.load(agent_json)
            agent.company_id = company_id

            if agent_json["password"]:
                hashed_password = custom_pbkdf2.hash(agent_json["password"])
                agent.password = hashed_password
                
            agent.save_to_db()

            return {"message":"Agent created!", "agent":agent_schema.dump(agent)}
        except Exception as e:
            print(str(e))
            return {"message":"An error has ocurred."}, 500


class AgentList (Resource):
    @classmethod
    @jwt_required
    def get (cls):

        claims = get_jwt_claims()
        company_id = claims.get("company_id")

        agents = AgentModel.get_agents(company_id)
        return agent_schema.dump(agents, many=True)

class AgentDeletion (Resource):
    @classmethod
    @jwt_required
    def delete(cls):
        ids = request.get_json()["ids"]

        task = TaskModel.find_by_agents(ids)

        if task:
            return {"message":"There are task with these agents"}, 400

        agents = AgentModel.get_many(ids)

        AgentModel.delete_many(ids)
        return {"message":"Agents deleted!"}

class AgentMassiveUpload (Resource):
    @classmethod
    @jwt_required
    def post (cls):
    
        claims = get_jwt_claims()
        company_id = claims.get("company_id")

        agents_json = request.get_json()["agents"]
        agents = agent_schema.load(agents_json, many=True) 
    
        for agent in agents:
            agent.company_id = company_id
            hashed_password = custom_pbkdf2.hash(agent.password)
            agent.password = hashed_password

        AgentModel.save_massive_to_db(agents)

        return {"message":"Agents added suscessfully"}

        
