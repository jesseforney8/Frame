from __init__ import db   
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.String(50))
    org = db.Column(db.String(20))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    goop = db.Column(db.String(1000))
    

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    urgency = db.Column(db.String(20))
    type = db.Column(db.String(20))
    owner = db.Column(db.String(20))
    submitter = db.Column(db.String(20))
    group = db.Column(db.String(20))
    org = db.Column(db.String(20))

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    org = db.Column(db.String(20))
    users = db.relationship("User", backref="group")







roles = {"r": "Reader", "e": "Editor", "m": "Manager"}

