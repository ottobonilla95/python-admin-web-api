from ma import ma
from models.production.user_setting import UserSettingModel

class UserSettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserSettingModel
        load_instance = True
        include_fk = True