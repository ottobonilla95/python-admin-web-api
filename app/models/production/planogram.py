from db import db
from datetime import datetime

class PlanogramModel (db.Model):

    __tablename__ = 'planogram'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship("CompanyModel", backref=db.backref('planograms', lazy=True, cascade="all, delete-orphan"))
    name = db.Column(db.String(40))
    description = db.Column(db.String(40))
    version = db.Column(db.Float)
    image = db.Column(db.String(150))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def find_by_id (cls, _id) -> "PlanogramModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_planograms (cls, _company_id) -> None:
        return cls.query.filter_by(company_id= _company_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
