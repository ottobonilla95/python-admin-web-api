from flask import request
from flask_restful import Resource

# models
from models import AgentModel

# schemas
from schemas.production.agent import AgentSchema

# hashlib
from passlib.hash import pbkdf2_sha256

# jwt
from flask_jwt_extended import create_access_token, create_refresh_token

agent_schema = AgentSchema()

custom_pbkdf2 = pbkdf2_sha256.using(rounds=296411)


class AgentLogin (Resource):
    @classmethod
    def post(cls):
        
        email_username = request.get_json()["email_username"]
        password = request.get_json()["password"]

        agentFound = AgentModel.find_by_username_or_email(email_username)

        if agentFound and custom_pbkdf2.verify(password, agentFound.password):
            
            access_token = create_access_token(identity=agentFound.id, fresh=True, expires_delta=False, user_claims={"company_id":agentFound.company_id})
            refresh_token = create_refresh_token(agentFound.id)

            return {
                "message":"Agent Logged In",
                "agent":{ 
                    "agent": {
                        **agent_schema.dump(agentFound)
                    } ,
                    "token":{
                        "access_token":access_token,
                        "refresh_token":refresh_token,
                    }
                },
            }

        return {"message":"Invalid credentials"}, 400