from db import db
from datetime import datetime

class CompanyModel (db.Model):

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    mobile_number = db.Column(db.String(20))
    address = db.Column(db.String(40))

    @classmethod
    def find_by_id (cls, _id) -> "CompanyModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name_or_email (cls, _name, _email) -> "CompanyModel":
        return cls.query.filter((cls.name == _name) | (cls.email == _email)).first()
    
    @classmethod
    def get_companies (cls) -> None:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
