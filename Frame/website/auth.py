from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
from models import User, roles
from flask_login import login_user, login_required, logout_user, current_user

def registerUser(email, fname, lname, password, org):
    new_user = User(email=email, firstname=fname, lastname=lname, password=generate_password_hash(password, method="scrypt"), role=roles["r"], org=org, groups="")

    db.session.add(new_user)
    db.session.commit()
    flash("Account created!", category="success")
    
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
def login():

    error = False
    error_type = "None"
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")


        user = User.query.filter_by(email=email).first()
        if email != "" or password != "":
            if user:
            
                if check_password_hash(user.password, password):
                    flash("Logged in!", category="success")
                    login_user(user, remember=True)
                    return redirect("/")
                else:
                    error = True
                    error_type = "invalid_password"
            else:
                error = True
                error_type = "user_doesnt_exist"
        else:
                error = True
                error_type = "info_not_filed_out"        
        


    return render_template("login.html", user=current_user, error=error, error_type=error_type)

@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():

    error = False
    error_type = "None"

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

            if user:
                error = True
                error_type = "user_already_exists"
            elif email == "" or firstname == "" or lastname == "" or password1 == "" or password2 == "":
                error = True
                error_type = "info_not_filed_out"
            elif password1 != password2:
                error = True
                error_type = "passwords_dont_match"
            elif len(password1) <= 8:
                error = True
                error_type = "passwords_too_short"
            elif len(email) < 6:
                error = True
                error_type = "email_too_short"
            elif len(firstname) < 2:
                error = True
                error_type = "name_too_short"
            elif len(lastname) < 2:
                error = True
                error_type = "lname_too_short"
            else:
                registerUser(email, firstname, lastname, password1, org)
                return redirect("/")
        
        except AttributeError:
            error = True
            error_type = "unknown_error"
            return redirect("/")

    return render_template("sign_up.html", user=current_user, error=error, error_type=error_type)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@auth.route("/settings", methods=["POST", "GET"])
@login_required
def settings():

    error = False
    error_type = "None"

    if request.method == "POST":
        newpassword = request.form.get("newpassword")
        newpassword2 = request.form.get("newpassword2")
        if newpassword != newpassword2:   
            error = True
            error_type = "passwords_dont_match"
        elif newpassword == "" and newpassword2 == "":
            error_type = "info_not_filed_out"
            error = True
        else:
            current_user.password = generate_password_hash(newpassword, method="scrypt")
            db.session.commit()
            flash("Password changed!", category="success")


    return render_template("settings.html", user=current_user, error=error, error_type=error_type)

@auth.route("/role", methods=["POST", "GET"])
@login_required
def role():
    if request.method == "POST":
        newrole = request.form.get("role")
        
        current_user.role = newrole
        db.session.commit()
        flash("Role changed!", category="success")


    return render_template("role.html", user=current_user)