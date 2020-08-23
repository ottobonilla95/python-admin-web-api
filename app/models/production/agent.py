from db import db
from datetime import datetime

class AgentModel (db.Model):

    __tablename__ = 'agent'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship("CompanyModel", backref=db.backref('agents', lazy=True, cascade="all, delete-orphan"))
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40))
    username = db.Column(db.String(20))
    password = db.Column(db.String(100))
    email = db.Column(db.String(40))
    mobile_number = db.Column(db.String(20))
    country = db.Column(db.String(40))
    image = db.Column(db.String(150))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def find_by_id (cls, _id) -> "AgentModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username_or_email (cls, _username_or_email) -> "AgentModel":
        return cls.query.filter((cls.username==_username_or_email) | (cls.email==_username_or_email)).first()

    @classmethod
    def get_agents (cls, _company_id) -> None:
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
    def save_massive_to_db(cls, agents):
        db.session.bulk_save_objects(agents)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
