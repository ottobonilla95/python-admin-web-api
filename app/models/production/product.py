from db import db
from datetime import datetime

class ProductModel (db.Model):

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship("CompanyModel", backref=db.backref('products', lazy=True, cascade="all, delete-orphan"))
    name = db.Column(db.String(60), nullable=False)
    upc = db.Column(db.String(20))
    category = db.Column(db.String(40))
    sub_category = db.Column(db.String(40))
    brand = db.Column(db.String(40))
    sub_brand = db.Column(db.String(40))
    container = db.Column(db.String(40))
    volume = db.Column(db.Float)
    width_size = db.Column(db.Float)
    height_size = db.Column(db.Float)
    image = db.Column(db.String(150))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def find_by_id (cls, _id) -> "ProductModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_products (cls, _company_id) -> None:
        return cls.query.filter_by(company_id= _company_id).all()

    @classmethod
    def get_many(cls, ids):
        return cls.query.filter(cls.id.in_(ids)).all()
        
    @classmethod
    def delete_many(cls, ids):
        delete_q = cls.__table__.delete().where(cls.id.in_(ids))
        db.session.execute(delete_q)
        db.session.commit()

    @classmethod
    def save_massive_to_db(cls, products):
        db.session.bulk_save_objects(products)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
