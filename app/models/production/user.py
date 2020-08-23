from db import db
from datetime import datetime

class UserModel (db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(100))
    profile_image = db.Column(db.String(150))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship("CompanyModel", backref=db.backref('users', lazy=True, cascade="all, delete-orphan"))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship("RoleModel", lazy=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def find_by_id (cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username (cls, _username) -> "UserModel":
        return cls.query.filter_by(username=_username).first()

    @classmethod
    def find_by_email (cls, _email) -> "UserModel":
        return cls.query.filter_by(email=_email).first()

    @classmethod
    def find_by_username_or_email (cls, _username, _email) -> "UserModel":
        return cls.query.filter((cls.username == _username) | (cls.email == _email)).first()

    @classmethod
    def get_users (cls, _company_id) -> None:
        return cls.query.filter_by(company_id=_company_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
