from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from models import Ticket, roles, User
from __init__ import db
import json

views = Blueprint("views", __name__)

@views.route("/", methods=["POST", "GET"])
@login_required
def home():
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







    return render_template("home.html", user=current_user)

@views.route("/tickets", methods=["POST", "GET"])
@login_required
def tickets():
    if request.method == "POST":
        ticket = json.loads(request.data)
        ticketId = ticket["ticketId"]
        tickettitle = ticket["title"]
        ticket = Ticket.query.get(ticketId)
        ticket.title = tickettitle
        db.session.commit()
        return jsonify({})

    return render_template("tickets.html", user=current_user, tickets=Ticket.query.filter_by(org="lantuesday.com"))

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
        print(email)
        if user.org == "":
            user.org = current_user.org
            db.session.commit()
            print(user.org, current_user.org)
        elif user.org == current_user.org:
            pass
        else:
            pass


    return render_template("members.html", user=current_user, members=User.query.filter_by(org=current_user.org))