from db import db

class UserSettingModel (db.Model):

    __tablename__ = 'user_setting'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column (db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("UserModel", backref=db.backref('profile_config', lazy=True, uselist=False, cascade="all, delete-orphan"))
    active_theme = db.Column (db.Integer, default=1)
    is_dark_sidenav = db.Column (db.Boolean, default=True)
    enable_sidebar_background_image = db.Column (db.Boolean, default=True)
    selected_sidebar_image = db.Column (db.String(50), default='/static/media/sidebar-4.34aa4bc1.jpg')
    mini_sidebar = db.Column (db.Boolean, default=False)
    box_layout = db.Column (db.Boolean, default=False)
    rtl_layout = db.Column (db.Boolean, default=False)
    dark_mode = db.Column (db.Boolean, default=False)
    language = db.Column (db.String(40))
    
    @classmethod
    def find_by_user_id (cls, _user_id) -> "UserSettingModel":
        return cls.query.filter_by(user_id=_user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
