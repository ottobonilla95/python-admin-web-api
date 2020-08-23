from ma import ma
from models import CompanyModel
from schemas.production.user import UserSchema

class CompanySchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CompanyModel
        load_instance = True

    users = ma.Nested(UserSchema, many=True)