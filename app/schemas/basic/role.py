from ma import ma
from models import RoleModel

class RoleSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel
        load_instance = True