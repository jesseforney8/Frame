from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
from models import User, roles
from flask_login import login_user, login_required, logout_user, current_user

def registerUser(email, fname, lname, password, org):
    new_user = User(email=email, firstname=fname, lastname=lname, password=generate_password_hash(password, method="sha256"), role=roles["r"], org=org)

    db.session.add(new_user)
    db.session.commit()
    flash("Account created!", category="success")
    
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category="success")
                login_user(user, remember=True)
                return redirect("/")
            else:
                flash("Inncorrect password!", category="error")
        else:
            flash("User doesn't exist!", category="error")
        


    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        org = ""
        print(email, firstname, lastname, password1, password2, org)
        

        user = User.query.filter_by(email=email).first()
        try:
            user1 = User.query.filter_by(org=org).first()
        

            if user:
                flash("User already exists!", category="error")
            elif password1 != password2:
                flash("Passwords do not match!", category="error")
            elif len(password1) <= 8:
                flash("Password must be greater than 8 character!", category="error")
            elif len(email) < 5:
                flash("E-mail must be greater than 5 characters!", category="error")
            elif len(firstname) < 1:
                flash("First Name must be greater than 1 character!", category="error")
            elif len(lastname) < 1:
                flash("Last Name must be greater than 1 character!", category="error")
            elif user1.org == "":
                registerUser(email, firstname, lastname, password1, org)
                return redirect("/")
            elif user1:
                flash("Org already exists!", category="error")
            else:
                registerUser(email, firstname, lastname, password1, org)
                return redirect("/")
        
        except AttributeError:
            registerUser(email, firstname, lastname, password1, org)
            return redirect("/")

    return render_template("sign_up.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@auth.route("/settings", methods=["POST", "GET"])
@login_required
def settings():
    if request.method == "POST":
        newpassword = request.form.get("newpassword")
        newpassword2 = request.form.get("newpassword2")
        if newpassword != newpassword2:
            flash("Passwords don't match!", category="error")    
        else:
            current_user.password = generate_password_hash(newpassword, method="sha256")
            db.session.commit()
            flash("Password changed!", category="success")


    return render_template("settings.html", user=current_user)

@auth.route("/role", methods=["POST", "GET"])
@login_required
def role():
    if request.method == "POST":
        newrole = request.form.get("role")
        
        current_user.role = newrole
        db.session.commit()
        flash("Role changed!", category="success")


    return render_template("role.html", user=current_user)