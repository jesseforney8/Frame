from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from models import Ticket, roles, User, Group, Comment
from __init__ import db
import json
from functions import ticket_lookup


views = Blueprint("views", __name__)

# route for the page that creates tickets

@views.route("/create", methods=["POST", "GET"])
@login_required
def create():
    error = False
    error_type = "None"
    
    if request.method == "POST":


        title = request.form.get("title")
        body = request.form.get("body")
        urgency = request.form.get("urgency")
        type_= request.form.get("type")
        submitter= request.form.get("submitter")
        org = current_user.org
        
        # minimum standard for creating ticket plus the db commit

        if len(title) < 5:
            error = True
            error_type = "title_too_short"
        elif len(body) < 5:
            error = True
            error_type = "body_too_short"
        elif len(submitter) < 5:
            error = True
            error_type = "submitter_too_short"
        elif type_ == None:
            error = True
            error_type = "select_a_type"
        elif urgency == None:
            error = True
            error_type = "select_a_urgency"
        elif title == "" or body == "" or submitter == "" or type_ == "" or urgency == "":
            error = True
            error_type = "info_not_filed_out"
        else:
            new_ticket = Ticket(title=title, body=body, urgency=urgency, type=type_, owner="Not Assigned", submitter=submitter, org=org, status="Open", comments="", group_id=0)
            db.session.add(new_ticket)
            db.session.commit()
            flash("Ticket Submitted!", category="success")

    return render_template("create.html", user=current_user, error=error, error_type=error_type)

#route for views tickets

@views.route("/tickets", methods=["POST", "GET"])
@login_required
def tickets():
    

    groups = Group.query.all()

    try:
        filter_info = session["filter_info"]

    except KeyError:
        return render_template("tickets.html", user=current_user, tickets=Ticket.query.filter_by(org=current_user.org), groups=groups)
    
    if filter_info["type_"] != "" and filter_info["filter_input"] != "":

        #filer for id
        if filter_info["type_"] == "id":
            try:
                ticket = Ticket.query.get(filter_info["filter_input"])
                if ticket == None:
                    return render_template("tickets.html", user=current_user, tickets=["No Tickets"], groups=groups)
                return render_template("tickets.html", user=current_user, tickets=[ticket], groups=groups)
            except UnboundLocalError:
                return redirect("/tickets")
        #filter for all
        elif filter_info["type_"] == "all":
            return render_template("tickets.html", user=current_user, tickets=Ticket.query.filter_by(org=current_user.org), groups=groups)
        #filer for group
        elif filter_info["type_"] == "group":
            group= Group.query.filter_by(name=filter_info["filter_input"]).first()

            tickets = Ticket.query.filter_by(group_id=group.id)
            return render_template("tickets.html", user=current_user, tickets=tickets , groups=groups)
        #filer for submitter
        elif filter_info["type_"] == "submitter":

            tickets = Ticket.query.filter_by(submitter=filter_info["filter_input"])
            return render_template("tickets.html", user=current_user, tickets=tickets , groups=groups)
        #filer for ownerS
        elif filter_info["type_"] == "owner":
            tickets = Ticket.query.filter_by(owner=filter_info["filter_input"])
            return render_template("tickets.html", user=current_user, tickets=tickets, groups=groups)
            
    return render_template("tickets.html", user=current_user, tickets=Ticket.query.filter_by(org=current_user.org), groups=groups)

@views.route(f"/ticket", methods=["POST", "GET"])
@login_required
def ticket():
    if request.method == "POST":
        ticketId = request.form.get("ticketId")
        comments = Comment.query.filter_by(ticket_id=ticketId)
        ticket = Ticket.query.filter_by(id=ticketId).first()
        session["ticket2"] = ticketId
        return render_template("ticket.html", user=current_user, ticket=ticket, comments=comments)
    if request.method == "GET":
        ticketId = session["ticket2"]
        comments = Comment.query.filter_by(ticket_id=ticketId)
        ticket = Ticket.query.filter_by(id=ticketId).first()
        return render_template("ticket.html", user=current_user, ticket=ticket, comments=comments)
    



# route to recieve json to delete ticket

@views.route("/delete-ticket", methods=["POST"])
def delete_ticket():
    ticket = json.loads(request.data)
    ticketId = ticket["ticketId"]
    ticket = Ticket.query.get(ticketId)
    if ticket:
        db.session.delete(ticket)
        db.session.commit()
            
    return jsonify({})

# route for members page

@views.route("/members", methods=["POST", "GET"])
@login_required
def members():

    #recieves json when admin tries to add a user to their org

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

            #restricts page access based on role
    groups = Group.query.all()
    if current_user.role == roles["a"] or current_user.role == roles["sa"]:
        return render_template("members.html", user=current_user, members=User.query.filter_by(org=current_user.org), groups=groups, glist = [])
    else:
        return render_template("home.html", user=current_user)
    

#route to recieve json to remove user from org

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

#route to change role of user
1
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

#route to add group to org        

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

#route to create org and also set original user to SA

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

 #route for homepage

@views.route("/", methods=["POST", "GET"])
@login_required
def home():
    if request.method == "POST":
        org = request.form.get("org")
        current_user.org = org
        current_user.role = "Super Administrator"
        db.session.commit()

        return render_template("home.html", user=current_user)



    return render_template("home.html", user=current_user)

@views.route("/filter", methods=["POST"])
@login_required
def filter():
    if request.method == "POST":
        filter_input = request.form.get("filter_input")
        type_ = request.form.get("type_")
        filter_info = {"filter_input": filter_input, "type_": type_}
        session["filter_info"] = filter_info

        return redirect("/tickets")

@views.route("/groups", methods=["POST", "GET"])
@login_required
def groups():
    ticketid = session["ticket_id_for_groups"]
    ticket = Ticket.query.filter_by(id=ticketid).first()

    if request.method == "POST":
        groupid = request.form.get("radio_group")
        
        ticket.group_id = groupid
        db.session.commit()
        return redirect("tickets")

    groups = Group.query.all()
    return render_template("groups.html", user=current_user, groups=groups, ticket=ticket.id)
    

@views.route("/get_ticket_id_for_group", methods=["POST"])
@login_required
def get_ticket_id_for_group():
    if request.method == "POST":
        ticketid = request.form.get("ticketId2")
        session["ticket_id_for_groups"] = ticketid
        return redirect("groups")

@views.route("/group_management", methods=["POST", "GET"])
@login_required
def group_management():

    groups = Group.query.all()

    if request.method == "POST":
        groupid = json.loads(request.data)
        group = Group.query.filter_by(id=groupid["groupId"]).first()
        db.session.delete(group)
        db.session.commit()
        return redirect("group_management")

    return render_template("group_management.html", user=current_user, groups=groups)



@views.route("/ticket_handler", methods=["POST"])
@login_required
def ticket_handler():
    if request.method == "POST":
       ticketid = session["ticket2"]
       ticket = Ticket.query.filter_by(id=ticketid).first()
       type_ = request.form.get("type_")
       
       if type_ == "title":
           return render_template("title_change.html", user=current_user, ticket=ticket)
       elif type_ == "body":
           return render_template("body_change.html", user=current_user, ticket=ticket)
       elif type_ == "owner":
           members = User.query.all()
           return render_template("owner_change.html", user=current_user, ticket=ticket.id, members=members)
       elif type_ == "submitter":
           members = User.query.all()
           return render_template("submitter_change.html", user=current_user, ticket=ticket.id, members=members)
       elif type_ == "status":
           return render_template("status_change.html", user=current_user, ticket=ticket.id)
       elif type_ == "type":
           return render_template("type_change.html", user=current_user, ticket=ticket)
       elif type_ == "urgency":
           return render_template("urgency_change.html", user=current_user, ticket=ticket)
       elif type_ == "group_name":
          groups = Group.query.all()
          return render_template("group_change.html", user=current_user, ticket=ticket.id, groups=groups )
       else:
           return redirect("tickets") 
       
@views.route("/title_change", methods=["POST"])
@login_required
def title_change():
    if request.method == "POST":
        ticket = ticket_lookup()

        title = request.form.get("title")
        ticket.title = title
        db.session.commit()
        return redirect("ticket")


@views.route("/body_change", methods=["POST"])
@login_required
def body_change():
    if request.method == "POST":
        ticket = ticket_lookup()

        body = request.form.get("body")
        ticket.body = body
        db.session.commit()
        return redirect("ticket")

@views.route("/owner_change", methods=["POST"])
@login_required
def owner_change():
    if request.method == "POST":
        ticket = ticket_lookup()
        member = request.form.get("radio_group")

        ticket.owner = member
        db.session.commit()
        return redirect("ticket")



@views.route("/submitter_change", methods=["POST"])
@login_required
def submitter_change():
    if request.method == "POST":
        ticket = ticket_lookup()
        member = request.form.get("radio_group")

        ticket.submitter = member
        db.session.commit()
        return redirect("ticket")

@views.route("/type_change", methods=["POST"])
@login_required
def type_change():
    if request.method == "POST":
        ticket = ticket_lookup()
        type_= request.form.get("type")

        ticket.type = type_

        db.session.commit()
        return redirect("ticket")



@views.route("/urgency_change", methods=["POST"])
@login_required
def urgency_change():
    if request.method == "POST":
        ticket = ticket_lookup()
        urgency = request.form.get("urgency")

        ticket.urgency = urgency

        db.session.commit()
        return redirect("ticket")

@views.route("/status_change", methods=["POST"])
@login_required
def status_change():
    if request.method == "POST":
        ticket = ticket_lookup()
        status = request.form.get("radio_group")
        print(status)

        ticket.status = status
        db.session.commit()
        return redirect("ticket")

@views.route("/group_change", methods=["POST"])
@login_required
def group_change():
    if request.method == "POST":
        ticket = ticket_lookup()
        groupid = request.form.get("radio_group")
        
        ticket.group_id = groupid
        db.session.commit()
        return redirect("ticket")
    
@views.route("/add_comment", methods=["POST"])
@login_required
def add_comment():
    if request.method =="POST":
        ticket = ticket_lookup()
        comment_text = request.form.get("comment_text_box")
        comment = Comment(text=comment_text, ticket_id=ticket.id)
        db.session.add(comment)
        db.session.commit()
        return redirect("ticket")
