from ma import ma
from models.production.customer import CustomerModel

class CustomerSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerModel
        load_instance = True
