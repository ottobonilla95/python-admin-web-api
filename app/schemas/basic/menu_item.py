from ma import ma
from models import MenuItemModel

class MenuItemSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MenuItemModel
        include_fk = True
        load_instance = True