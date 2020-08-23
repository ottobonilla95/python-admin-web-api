from flask import Blueprint
from flask_restful import Api

# resources
from resources.agent import Agent, AgentCreation, AgentDeletion, AgentList, AgentMassiveUpload

agent_module = Blueprint('agent_module', __name__)
api = Api(agent_module)

api.add_resource(Agent, '/<string:id>')
api.add_resource(AgentCreation, '/create')
api.add_resource(AgentDeletion, '/delete')
api.add_resource(AgentList, '/list')
api.add_resource(AgentMassiveUpload, '/massive')


