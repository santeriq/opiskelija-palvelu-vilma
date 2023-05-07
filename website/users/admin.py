from flask import Blueprint, redirect, render_template, flash, request, jsonify, session, abort
from flask_login import login_required, current_user
import json
import website.database as database
import website.functions as functions

admin = Blueprint("admin", __name__)


@admin.route("/create-course", methods=["GET", "POST"])
@login_required
def create_course():
    if current_user.role == "admin":
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
               abort(403)
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
        return render_template("admin/tools/create_course.html", user=current_user)
    return redirect("/")


@admin.route("/edit-courses", methods=["GET", "POST"])
@login_required
def edit_courses():
    if current_user.role == "admin":
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
               abort(403)
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
        return render_template("admin/tools/edit_courses.html", user=current_user)
    return redirect("/")


@admin.route("/view-role-requests")
@login_required
def view_role_requests():
    if current_user.role == "admin" or current_user.role == "teacher":
        requests = database.get_role_requests_list()
        count = len(requests)
        return render_template("admin/tools/view_role_requests.html", count=count, requests=requests, user=current_user)
    return redirect("/")

@admin.route("/accept-request", methods=["POST"])
@login_required
def accept_request():
    data = json.loads(request.data)
    username = data["username"]
    check = functions.new_username(username)
    if check is False:
        database.accept_role_request(username)
        flash(f"Hyväksyttiin {username} pyyntö", category="success")
    return jsonify({})
    
@admin.route("/reject-request", methods=["POST"])
@login_required
def reject_request():
    data = json.loads(request.data)
    username = data["username"]
    check = functions.new_username(username)
    if check is False:
        database.reject_role_request(username)
        flash(f"Hylättiin {username} pyyntö", category="error")
    
    return jsonify({})

@admin.route("/manage-users", methods=["GET", "POST"])
@login_required
def manage_users():
    if current_user.role == "admin":
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
               abort(403)
            username = request.form.get("username")
            role = request.form.get("user_role")
            delete = request.form.get("delete")
            if functions.new_username(username) is True:
                flash(f"Käyttäjää {username} ei löytynyt", category="error")
            elif delete == "POISTA":
                database.delete_user(username)
                flash(f"Poistettiin käyttäjä {username}", category="success")
            elif role == "Opiskelija":
                database.set_user_role(username, "student")
                flash(f"Päivitettiin {username} opiskelijaksi", category="success")
            elif role == "Opettaja":
                database.set_user_role(username, "teacher")
                flash(f"Päivitettiin {username} opettajaksi", category="success")
            elif role == "Admin":
                database.set_user_role(username, "admin")
                flash(f"Päivitettiin {username} ylläpitäjäksi", category="success")
            elif role == "None":
                database.set_user_role(username, "none")
                flash(f"Käyttäjällä {username} ei ole enään mitään roolia", category="success")
        return render_template("admin/tools/manage_users.html", user=current_user)
    return redirect("/")


@admin.route("/view-users/sorted-by-id")
@login_required
def view_users_sorted_by_id():
    if current_user.role == "admin":
        users = database.get_users_list_sorted_by("id")
        return render_template("admin/tools/view_users/id.html", users_list=users, user=current_user)
    return redirect("/")

@admin.route("/view-users/sorted-by-id-desc")
@login_required
def view_users_sorted_by_id_desc():
    if current_user.role == "admin":
        users = database.get_users_list_sorted_by("id", True)
        return render_template("admin/tools/view_users/id_desc.html", users_list=users, user=current_user)
    return redirect("/")

@admin.route("/view-users/sorted-by-username")
@login_required
def view_users_sorted_by_username():
    if current_user.role == "admin":
        users = database.get_users_list_sorted_by("username")
        return render_template("admin/tools/view_users/username.html", users_list=users, user=current_user)
    return redirect("/")

@admin.route("/view-users/sorted-by-username-desc")
@login_required
def view_users_sorted_by_username_desc():
    if current_user.role == "admin":
        users = database.get_users_list_sorted_by("username", True)
        return render_template("admin/tools/view_users/username_desc.html", users_list=users, user=current_user)
    return redirect("/")



@admin.route("/view-students/sorted-by-id")
@login_required
def view_students_sorted_by_id():
    if current_user.role == "admin":
        users = database.get_students_list_sorted_by("id")
        return render_template("admin/tools/view_students/id.html", users_list=users, user=current_user)
    return redirect("/")

@admin.route("/view-students/sorted-by-id-desc")
@login_required
def view_students_sorted_by_id_desc():
    if current_user.role == "admin":
        users = database.get_students_list_sorted_by("id", True)
        return render_template("admin/tools/view_students/id_desc.html", users_list=users, user=current_user)
    return redirect("/")

@admin.route("/view-students/sorted-by-username")
@login_required
def view_students_sorted_by_username():
    if current_user.role == "admin":
        users = database.get_students_list_sorted_by("username")
        return render_template("admin/tools/view_students/username.html", users_list=users, user=current_user)
    return redirect("/")

@admin.route("/view-students/sorted-by-username-desc")
@login_required
def view_students_sorted_by_username_desc():
    if current_user.role == "admin":
        users = database.get_students_list_sorted_by("username", True)
        return render_template("admin/tools/view_students/username_desc.html", users_list=users, user=current_user)
    return redirect("/")

@admin.route("/view-students/sorted-by-credits")
@login_required
def view_students_sorted_by_credits():
    if current_user.role == "admin":
        users = database.get_students_list_sorted_by("credits")
        return render_template("admin/tools/view_students/credits.html", users_list=users, user=current_user)
    return redirect("/")

@admin.route("/view-students/sorted-by-credits-desc")
@login_required
def view_students_sorted_by_credits_desc():
    if current_user.role == "admin":
        users = database.get_students_list_sorted_by("credits", True)
        return render_template("admin/tools/view_students/credits_desc.html", users_list=users, user=current_user)
    return redirect("/")


@admin.route("/view-courses/sorted-by-name")
@login_required
def view_courses():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        courses = database.get_courses_list_sorted_by("name")
        return render_template("admin/tools/view_courses/name.html", courses=courses, user=current_user)
    return redirect("/")

@admin.route("/view-courses/sorted-by-name-desc")
@login_required
def view_courses_desc():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        courses = database.get_courses_list_sorted_by("name", True)
        return render_template("admin/tools/view_courses/name_desc.html", courses=courses, user=current_user)
    return redirect("/")

@admin.route("/view-courses/sorted-by-credits")
@login_required
def view_courses_sorted_by_credits():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        courses = database.get_courses_list_sorted_by("credits")
        return render_template("admin/tools/view_courses/credits.html", courses=courses, user=current_user)
    return redirect("/")

@admin.route("/view-courses/sorted-by-credits-desc")
@login_required
def view_courses_sorted_by_credits_desc():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        courses = database.get_courses_list_sorted_by("credits", True)
        return render_template("admin/tools/view_courses/credits_desc.html", courses=courses, user=current_user)
    return redirect("/")

@admin.route("/view-courses/sorted-by-key")
@login_required
def view_courses_sorted_by_key():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        courses = database.get_courses_list_sorted_by("key")
        return render_template("admin/tools/view_courses/key.html", courses=courses, user=current_user)
    return redirect("/")

@admin.route("/view-courses/sorted-by-key-desc")
@login_required
def view_courses_sorted_by_key_desc():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        courses = database.get_courses_list_sorted_by("key", True)
        return render_template("admin/tools/view_courses/key_desc.html", courses=courses, user=current_user)
    return redirect("/")

@admin.route("/view-courses/sorted-by-status")
@login_required
def view_courses_sorted_by_status():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        courses = database.get_courses_list_sorted_by("open")
        return render_template("admin/tools/view_courses/status.html", courses=courses, user=current_user)
    return redirect("/")

@admin.route("/view-courses/sorted-by-status-desc")
@login_required
def view_courses_sorted_by_status_desc():
    if current_user.role == "admin" or current_user.role == "teacher" or current_user.role == "student":
        courses = database.get_courses_list_sorted_by("open", True)
        return render_template("admin/tools/view_courses/status_desc.html", courses=courses, user=current_user)
    return redirect("/")


