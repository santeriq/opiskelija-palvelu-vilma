from flask import Blueprint, redirect, render_template, flash, url_for, request, jsonify
from flask_login import login_required, current_user
import json
import website.database as database
import website.functions as functions

routes = Blueprint("routes", __name__)



@routes.route("/")
@login_required
def home():
    if current_user.role == "admin":
        return redirect(url_for("routes.admin"))
    elif current_user.role == "teacher":
        return redirect(url_for("routes.teacher"))
    elif current_user.role == "student":
        return redirect(url_for("routes.teacher"))
    elif current_user.role == "none":
        return redirect(url_for("routes.guest"))
    return render_template("home.html", user=current_user)

@routes.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    return render_template("logged_in_admin.html", user=current_user)

@routes.route("/teacher")
@login_required
def teacher():
    return render_template("logged_in_teacher.html", user=current_user)

@routes.route("/student")
@login_required
def student():
    return render_template("logged_in_student.html", user=current_user)

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
    return render_template("logged_in_guest.html", user=current_user)

@routes.route("/create-course", methods=["GET", "POST"])
@login_required
def create_course():
    if current_user.role == "admin":
        if request.method == "POST":
            course_name = request.form.get("course_name")
            course_credits = request.form.get("course_credits")
            course_key = request.form.get("course_key")
            if len(course_name) < 5:
                flash("Kurssimimen tulee olla vähintään 5 merkkiä", category="error")
            elif len(course_name) > 70:
                flash("Kurssinimen tulee olla enintään 70 merkkiä", category="error")
            elif str(course_credits).isdigit() is False:
                flash("Kurssin opintopistemäärän tulee olla kokonaisluku", category="error")
            elif len(course_key) < 5:
                flash("Kurssiavain tulee olla vähintään 5 merkkiä", category="error")
            elif len(course_key) > 20:
                flash("Kurssiavain tulee olla enintään 20 merkkiä", category="error")
            elif functions.new_course_key(course_key) is False:
                flash("Kurssiavain ei ole vapaana", category="error")
            else:
                database.create_course(course_key, course_name, int(course_credits))
                flash(f'Luotiin uusi kurssi nimellä "{course_name}"', category="success")
        return render_template("create_course.html", user=current_user)
    return redirect("/")

@routes.route("/view-courses")
@login_required
def view_courses():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        return render_template("view_courses.html", courses=database.get_courses_list_sorted_by_name(), user=current_user)
    return redirect("/")

@routes.route("/view-courses/sorted-by-credits")
@login_required
def view_courses_sorted_by_credits():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        return render_template("view_courses.html", courses=database.get_courses_list_sorted_by_credits(), user=current_user)
    return redirect("/")

@routes.route("/view-courses/sorted-by-key")
@login_required
def view_courses_sorted_by_key():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        return render_template("view_courses.html", courses=database.get_courses_list_sorted_by_key(), user=current_user)
    return redirect("/")

@routes.route("/view-courses/sorted-by-status")
@login_required
def view_courses_sorted_by_status():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        return render_template("view_courses.html", courses=database.get_courses_list_sorted_by_open(), user=current_user)
    return redirect("/")

@routes.route("/edit-courses", methods=["GET", "POST"])
@login_required
def edit_courses():
    if current_user.role == "admin":
        if request.method == "POST":
            course_name = request.form.get("course_name")
            course_credits = request.form.get("course_credits")
            course_key = request.form.get("course_key")
            course_status = request.form.get("course_status")
            if course_status == "Avoin":
                course_status = "true"
            elif course_status == "Suljettu":
                course_status = "false"
            if functions.new_course_key(course_key):
                flash("Kurssiavainta ei löytynyt", category="error")
            elif len(course_name) < 5:
                flash("Kurssimimen tulee olla vähintään 5 merkkiä", category="error")
            elif len(course_name) > 70:
                flash("Kurssinimen tulee olla enintään 70 merkkiä", category="error")
            elif str(course_credits).isdigit() is False:
                flash("Kurssin opintopistemäärän tulee olla kokonaisluku", category="error")
            elif len(course_key) < 5:
                flash("Kurssiavain tulee olla vähintään 5 merkkiä", category="error")
            elif len(course_key) > 20:
                flash("Kurssiavain tulee olla enintään 20 merkkiä", category="error")
            else:
                database.update_course(course_key, course_name, int(course_credits), course_status)
                flash(f'Päivitettiin kurssi jonka avain on "{course_key}"', category="success")
        return render_template("edit_courses.html", user=current_user)
    return redirect("/")


@routes.route("/view-role-requests")
@login_required
def view_role_requests():
    if current_user.role == "admin" or current_user.role == "teacher":
        return render_template("view_role_requests.html", requests=database.get_role_requests_list(), user=current_user)
    return redirect("/")

@routes.route("/accept-request", methods=["POST"])
@login_required
def accept_request():
    data = json.loads(request.data)
    print(data)
    username = data["username"]
    print(username)
    check = functions.new_username(username)
    if check is False:
       # database.accept_role_request(username)
        flash(f"Hyväksyttiin {username} pyyntö", category="success")
    
    return jsonify({})
    
@routes.route("/reject-request", methods=["POST"])
@login_required
def reject_request():
    data = json.loads(request.data)
    username = data["username"]
    print(username)
    check = functions.new_username(username)
    if check is False:
       # database.reject_role_request(username)
        flash(f"Hylättiin {username} pyyntö", category="error")
    
    return jsonify({})
