from __init__ import db   
from flask_login import UserMixin



user_groups = db.Table("user_groups",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"))

)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.String(50))
    org = db.Column(db.String(20))
    groups = db.relationship("Group", secondary=user_groups, backref="groups")

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
    status = db.Column(db.String(20))
    platform = db.Column(db.String(20))
    version = db.Column(db.String(20))
    comments = db.Column(db.String(500))
    due_date = db.Column(db.String(20))
    score = db.Column(db.String(20))
    update_time = db.Column(db.String(20))
    attachments = db.Column(db.String(20))
    followers = db.Column(db.String(20))
    resoltion_notes = db.Column(db.String(20))
    r_approver = db.Column(db.String(20))
    projected_time = db.Column(db.String(20))
    spent_time = db.Column(db.String(20))
    ticket_history = db.Column(db.String(20))
    org = db.Column(db.String(20))

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    org = db.Column(db.String(20))







roles = {"r": "Reader", "e": "Editor", "a": "Administrator", "sa": "Super Administrator"}

