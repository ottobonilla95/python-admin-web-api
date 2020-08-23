from ma import ma
from models.production.agent import AgentModel

class AgentSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AgentModel
        load_instance = True
        load_only=("password",)