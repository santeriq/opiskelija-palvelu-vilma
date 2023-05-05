from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import login_required, current_user
import website.database as database
import website.functions as functions

routes = Blueprint("routes", __name__)


@routes.route("/")
@login_required
def home():
    if current_user.role == "admin":
        return redirect(("/admin"))
    elif current_user.role == "teacher":
        return redirect("/teacher")
    elif current_user.role == "student":
        return redirect("/student")
    elif current_user.role == "none":
        return redirect("/guest")

@routes.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    return render_template("admin/logged_in.html", user=current_user)

@routes.route("/teacher")
@login_required
def teacher():
    return render_template("teacher/logged_in.html", user=current_user)

@routes.route("/student")
@login_required
def student():
    return render_template("student/logged_in.html", user=current_user)

@routes.route("/guest", methods=["GET", "POST"])
@login_required
def guest():
    if request.method == "POST":
        username = current_user.username
        message = request.form.get("message")
        check_new_request = functions.new_role_request(username)
        if len(message) > 200:
            flash("Viesti liian pitkä", category="error")
        elif check_new_request:
            database.create_role_request(username, message)
            flash("Pyyntö lähetetty", category="success")
        else:
            database.update_role_request(username, message)
            flash("Pyyntö päivitetty", category="success")
    return render_template("guest/logged_in.html", user=current_user)
