from flask import Blueprint, redirect, render_template, flash, request, session, abort
from flask_login import login_required, current_user
import website.database as database
import website.functions as functions
from .users import teacher as teacher_module

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

@routes.route("/admin")
@login_required
def admin():
    if current_user.role == "admin":
        return render_template("admin/logged_in.html", user=current_user)
    return redirect("/")

@routes.route("/teacher", methods=["GET", "POST"])
@login_required
def teacher():
    username = current_user.username
    if current_user.role == "teacher":
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
               abort(403)
            key = request.form.get("course_key").lower()
            if functions.new_course_key(key):
                flash("Kurssiavainta ei löytynyt", category="error")
            elif functions.check_is_in_course(key, username) is False:
                flash("Et ole kurssilla", category="error")
            else:
                return teacher_module.manage_course(key)
        return render_template("teacher/logged_in.html", user=current_user)
    return redirect("/")

@routes.route("/student")
@login_required
def student():
    if current_user.role == "student":
        username = current_user.username
        gpa = database.get_student_gpa(username)
        gpa = f"{gpa:.2f}"
        credits = int(database.get_student_credits(username))
        credits = f"{credits:.2f}"
        return render_template("student/logged_in.html", gpa=gpa, credits=credits, user=current_user)
    return redirect("/")

@routes.route("/guest", methods=["GET", "POST"])
@login_required
def guest():
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
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
