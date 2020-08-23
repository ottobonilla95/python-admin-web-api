from ma import ma
from models.production.product import ProductModel

class ProductSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel
        load_instance = True