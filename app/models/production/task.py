from db import db
from datetime import datetime

class TaskModel (db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship("CompanyModel", backref=db.backref('tasks', lazy=True, cascade="all, delete-orphan"))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship("CustomerModel", backref=db.backref('tasks', lazy=True, cascade="all, delete-orphan"))
    planogram_id = db.Column(db.Integer, db.ForeignKey('planogram.id'), nullable=False)
    planogram = db.relationship("PlanogramModel")
    start_before = db.Column(db.DateTime)
    complete_before = db.Column(db.DateTime)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
    agent = db.relationship("AgentModel")
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
        
    @classmethod
    def find_by_id (cls, _id) -> "TaskModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_tasks (cls, _company_id) -> None:
        return cls.query.filter_by(company_id= _company_id).all()

    @classmethod
    def find_by_planogram (cls, _planogram_id) -> None:
        return cls.query.filter_by(planogram_id= _planogram_id).first()

    @classmethod
    def find_by_agents (cls, _agent_ids) -> None:
        return cls.query.filter(cls.agent_id.in_(_agent_ids)).first()

    @classmethod
    def delete_many(cls, ids):
        delete_q = cls.__table__.delete().where(cls.id.in_(ids))
        db.session.execute(delete_q)
        db.session.commit()

    @classmethod
    def delete_by_customer(cls, ids):
        delete_q = cls.__table__.delete().where(cls.customer_id.in_(ids))
        db.session.execute(delete_q)
        db.session.commit()

    @classmethod
    def save_massive_to_db(cls, tasks):
        db.session.bulk_save_objects(tasks)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
