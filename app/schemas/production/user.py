from ma import ma
from models.production.user import UserModel
from schemas.production.user_setting import UserSettingSchema
from schemas.basic.role import RoleSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        include_fk = True
        load_only = ("password",)
        
    role = ma.Nested(RoleSchema)