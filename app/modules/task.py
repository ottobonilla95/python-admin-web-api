from flask import Blueprint
from flask_restful import Api

# resources
from resources.task import Task, TaskCreation, TaskDeletion, TaskList, TaskMassiveUpload


task_module = Blueprint('task_module', __name__)
api = Api(task_module)

api.add_resource(Task, '/<string:id>')
api.add_resource(TaskCreation, '/create')
api.add_resource(TaskDeletion, '/delete')
api.add_resource(TaskList, '/list')
api.add_resource(TaskMassiveUpload, '/massive')



