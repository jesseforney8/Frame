from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from models import Ticket, roles, User, Group
from __init__ import db
import json


views = Blueprint("views", __name__)


@views.route("/create", methods=["POST", "GET"])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        urgency = request.form.get("urgency")
        type= request.form.get("type")
        owner= request.form.get("owner")
        submitter= request.form.get("submitter")
        org = current_user.org
        
        if len(title) < 5:
            flash("Title too small!", category="error")
        elif len(body) < 5:
            flash("Body too small!", category="error")
        elif len(owner) < 5:
            flash("Owner too small!", category="error")
        elif len(submitter) < 5:
            flash("Submitter too small!", category="error")
        elif len(urgency) < 3:
            flash("Select an urgency", category="error")
        elif len(type) < 3:
            flash("Select an type", category="error")
        else:
            new_ticket = Ticket(title=title, body=body, urgency=urgency, type=type, owner=owner, submitter=submitter, org=org)
            db.session.add(new_ticket)
            db.session.commit()
            flash("Ticket Submitted!", category="success")







    return render_template("create.html", user=current_user)

@views.route("/tickets", methods=["POST", "GET"])
@login_required
def tickets():
    if request.method == "POST":
        ticket = json.loads(request.data)

        ticketId = ticket["ticketId"]
        session["id"] = ticketId       

        return jsonify({})
        
    
    return render_template("tickets.html", user=current_user, tickets=Ticket.query.filter_by(org=current_user.org))
    


@views.route(f"/ticket", methods=["POST", "GET"])
@login_required
def ticket():
    if request.method == "POST":
        ticket = json.loads(request.data)

        ticketId = ticket["ticketId"]
        tickettitle = ticket["title"]
        ticketbody = ticket["body"]
        ticketowner = ticket["owner"]
        ticketsubmitter = ticket["submitter"]
        tickettype = ticket["type"]
        ticketurgency = ticket["urgency"]
        

        ticket = Ticket.query.get(ticketId)

        ticket.owner = ticketowner
        ticket.title = tickettitle
        ticket.body = ticketbody
        ticket.submitter = ticketsubmitter
        ticket.type = tickettype
        ticket.urgency = ticketurgency

        db.session.commit()
        return jsonify({})
    
    return render_template("/ticket.html", user=current_user, tickets=Ticket.query.filter_by(id=session.get("id")))

    

@views.route("/delete-ticket", methods=["POST"])
def delete_ticket():
    ticket = json.loads(request.data)
    ticketId = ticket["ticketId"]
    ticket = Ticket.query.get(ticketId)
    if ticket:
        db.session.delete(ticket)
        db.session.commit()
            
    return jsonify({})

@views.route("/members", methods=["POST", "GET"])
@login_required
def members():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        
        if user.org == "":
            user.org = current_user.org
            db.session.commit()
            
        elif user.org == current_user.org:
            pass
        else:
            pass

    return render_template("members.html", user=current_user, members=User.query.filter_by(org=current_user.org), groups=Group.query.filter_by(org=current_user.org), glist = [])

    

@views.route("/removeorg", methods=["POST"])
@login_required
def removeorg():
    if request.method == "POST":
        usersubmit = json.loads(request.data)
        email = usersubmit["email"]
        
        user = User.query.filter_by(email=email).first()
        user.org = ""
        
        db.session.commit()
        return jsonify({})

@views.route("/changerole", methods=["POST"])
@login_required
def changerole():
    if request.method == "POST":
        usersubmit = json.loads(request.data)
        email = usersubmit["email"]
        role = usersubmit["role"]
        
        user = User.query.filter_by(email=email).first()
        user.role = role
        
        db.session.commit()
        return jsonify({})

@views.route("/addgroup", methods=["POST"])
@login_required
def addgroup():
    if request.method == "POST":
        usersubmit = json.loads(request.data)
        group = usersubmit["group"]
        
        
        grp = Group(name=group, org=current_user.org)
        
        db.session.add(grp)
        db.session.commit()
        return jsonify({})

@views.route("/createorg", methods=["POST"])
@login_required
def createorg():
    if request.method == "POST":
        usersubmit = json.loads(request.data)
        org = usersubmit["org"]
        current_user.org = org
        current_user.role = roles["sa"]
        db.session.commit()
        return jsonify({})
@views.route("/", methods=["POST", "GET"])
@login_required
def home():
    return render_template("home.html", user=current_user)