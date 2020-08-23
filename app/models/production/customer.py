from db import db
from datetime import datetime

class CustomerModel (db.Model):

    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship("CompanyModel", backref=db.backref('customers', lazy=True, cascade="all, delete-orphan"))
    name = db.Column(db.String(60), nullable=False)
    mobile_number = db.Column(db.String(20))
    email = db.Column(db.String(40))
    country = db.Column(db.String(40))
    state = db.Column(db.String(40))
    street_name = db.Column(db.String(40), nullable=False)
    postal_code = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def find_by_id (cls, _id) -> "CustomerModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def get_customers (cls, _company_id) -> None:
        return cls.query.filter_by(company_id= _company_id).all()

    @classmethod
    def delete_many(cls, ids):
        delete_q = cls.__table__.delete().where(cls.id.in_(ids))
        db.session.execute(delete_q)
        db.session.commit()

    @classmethod
    def save_massive_to_db(cls, customers):
        db.session.bulk_save_objects(customers)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
