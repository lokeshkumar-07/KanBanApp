from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin



db = SQLAlchemy()



roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    lists = db.relationship('Lists', backref='user', lazy=True)


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Lists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review = db.Column(db.String, default = 'Not Reviewed Yet')
    created_date = db.Column(db.String)
    lcard = db.relationship('Cards', cascade='all, delete-orphan', backref='card')
    

class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable = False)
    deadline = db.Column(db.String, nullable = False)
    mark = db.Column(db.String, default="Not Complected")
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable= False)
    complete_date = db.Column(db.String, default = None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 