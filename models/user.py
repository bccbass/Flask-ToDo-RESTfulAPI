from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80))
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String())


    tasks = db.relationship('Task', back_populates='user')

class UserSchema(ma.Schema):
    tasks = fields.List(fields.Nested('TaskSchema', exclude=['user']))
    class Meta:
        fields = ('name', 'email', 'id', 'password', 'tasks')
        ordered = True
