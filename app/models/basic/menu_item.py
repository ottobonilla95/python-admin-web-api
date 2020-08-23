from db import db

class MenuItemModel(db.Model):

    __tablename__ = 'menu_item'

    id = db.Column (db.Integer, primary_key=True)
    menu_title = db.Column (db.String(30), nullable=False)
    menu_icon = db.Column (db.String(40))
    path = db.Column (db.String(60))
    new_item =db.Column (db.Boolean) 
    sequence =db.Column (db.Integer) 
    father_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))


    @classmethod
    def get_menu(cls, _role):
        query = cls.query\
                    .join(MenuItemByRoleModel, cls.id == MenuItemByRoleModel.menu_item_id)\
                    .filter(MenuItemByRoleModel.role_id == _role)\
                    .order_by(cls.sequence.asc())

        return query.all()
                

class MenuItemByRoleModel(db.Model):

    __tablename__ = 'menu_item_by_role'

    id = db.Column (db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))