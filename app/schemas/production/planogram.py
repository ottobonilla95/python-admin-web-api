from ma import ma
from models.production.planogram import PlanogramModel

class PlanogramSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlanogramModel
        load_instance = True