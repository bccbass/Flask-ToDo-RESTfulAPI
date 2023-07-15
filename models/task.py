from init import db, ma
from marshmallow import fields

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    details = db.Column(db.Text())
    status = db.Column(db.String(20))
    date_created = db.Column(db.Date())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    user = db.relationship('User', back_populates='tasks')

class TaskSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['password', 'tasks', 'email'])

    class Meta:
        fields = ('id', 'title', 'details', 'status', 'date_created', 'user')
        ordered = True
