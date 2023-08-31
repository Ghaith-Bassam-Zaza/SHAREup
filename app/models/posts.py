from datetime import datetime
from . import db


class Post(db.Model):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    body =db.Column(db.String(255))
    time_stamp =db.Column(db.DateTime(),default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))