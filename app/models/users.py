from . import db, ma
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    email =db.Column(db.String(255), unique = True)
    name =db.Column(db.String(255))
    pswrd =db.Column(db.String(255))
    posts = db.relationship('Post',backref='author',lazy=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ['email','name']


userSchema = UserSchema();
usersSchema = UserSchema(many= True);