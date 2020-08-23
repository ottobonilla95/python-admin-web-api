from flask_restful import Resource
from models import MenuItemModel

# jwt
from flask_jwt_extended import jwt_required, get_jwt_claims

# schemas
from schemas.basic.menu_item import MenuItemSchema

menu_item_schema = MenuItemSchema()

class Menu (Resource):
    @classmethod
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        role = claims.get('role')

        menu = MenuItemModel.get_menu(role)

        return {"menu":menu_item_schema.dump(menu, many=True)}
