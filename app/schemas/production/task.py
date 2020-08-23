from ma import ma
from models.production.task import TaskModel

class Taskchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskModel
        load_instance = True
        include_fk = True