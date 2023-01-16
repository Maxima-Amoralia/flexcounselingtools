from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    note = db.relationship('Note')
    ca_activity = db.relationship('CA_Activity')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    #date = db.Column(db.DateTime(timezone=True), default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class CA_Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    activity_type = db.Column(db.String(100))
    position = db.Column(db.String(200))
    organization = db.Column(db.String(400))
    description = db.Column(db.String(600))
#    grade9 = db.Column(db.Boolean)
#    grade10 = db.Column(db.Boolean)
#    grade11 = db.Column(db.Boolean)
#    grade12 = db.Column(db.Boolean)
#    grade_post = db.Column(db.Boolean)
#    time_school = db.Column(db.Boolean)
#    time_break = db.Column(db.Boolean)
#    time_all = db.Column(db.Boolean)
#    hours = db.Column(db.Integer)
#    weeks = db.Column(db.Integer)
#    participate = db.Column(db.Boolean)
#    feedback = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class UCActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
