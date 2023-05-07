from flask import Blueprint, redirect, render_template, flash, request, jsonify
from flask_login import login_required, current_user
import json
import website.database as database
import website.functions as functions

student = Blueprint("student", __name__)



@student.route("/join-course", methods=["GET", "POST"])
@login_required
def join_course():
    role = current_user.role
    if role == "admin" or role == "teacher" or role == "student":
        if request.method == "POST":
            username = current_user.username
            course_key = request.form.get("course_key").lower()
            confirm = request.form.get("confirm")
            new_key = functions.new_course_key(course_key)
            if new_key is True:
                flash(f'Liittyminen epäonnistui, kurssiavainta "{course_key}" ei löytynyt', category="error")
            elif confirm != "LIITY":
                flash(f"Liittyminen epäonnistui", category="error")
            elif functions.check_course_open(course_key) is False:
                flash("Liittyminen epäonnistui, kurssi ei ole auki", category="error")
            elif functions.check_is_in_course(course_key, username) is True:
                flash(f'Liittyminen epäonnistui, olet jo kurssilla "{course_key}"', category="error")
            else:
                database.join_course(course_key, username)
                flash(f'Liityttiin kurssille "{course_key}"')
        return render_template("teacher/tools/join_course.html", user=current_user)
    return redirect("/")

@student.route("/leave-course", methods=["GET", "POST"])
@login_required
def leave_course():
    role = current_user.role
    if role == "admin" or role == "teacher" or role == "student":
        if request.method == "POST":
            username = current_user.username
            course_key = request.form.get("course_key").lower()
            confirm = request.form.get("confirm")
            new_key = functions.new_course_key(course_key)
            if new_key is True:
                flash(f'Kurssiavainta "{course_key}" ei löytynyt', category="error")
            elif confirm != "POISTU":
                flash(f"Poistuminen epäonnistui", category="error")
            elif functions.check_is_in_course(course_key, username) is False:
                flash(f'Poistuminen epäonnistui, et ole kurssilla "{course_key}"', category="error")
            else:
                database.leave_course(course_key, username)
                flash(f'Poistuit kurssilta "{course_key}"')
        return render_template("teacher/tools/leave_course.html", user=current_user)
    return redirect("/")


@student.route("/view-my-courses")
@login_required
def view_my_courses():
    role = current_user.role
    username = current_user.username
    if role == "admin" or role == "teacher" or role == "student":
        my_courses = database.get_user_courses(username)
        return render_template("teacher/tools/view_my_courses.html", courses_list=my_courses, user=current_user)
    return redirect("/")


@student.route("/view-credits/sorted-by-grade")
@login_required
def view_credits_sorted_by_grade():
    role = current_user.role
    username = current_user.username
    if role == "student":
        credits = database.get_student_completed_courses_sorted_by(username, "grade", False)
        return render_template("student/tools/view_credits/grade.html", credits=credits, user=current_user)
    return redirect("/")

@student.route("/view-credits/sorted-by-grade-desc")
@login_required
def view_credits_sorted_by_grade_desc():
    role = current_user.role
    username = current_user.username
    if role == "student":
        credits = database.get_student_completed_courses_sorted_by(username, "grade", True)
        return render_template("student/tools/view_credits/grade_desc.html", credits=credits, user=current_user)
    return redirect("/")

@student.route("/view-credits/sorted-by-credits")
@login_required
def view_credits_sorted_by_credits():
    role = current_user.role
    username = current_user.username
    if role == "student":
        credits = database.get_student_completed_courses_sorted_by(username, "credits", False)
        return render_template("student/tools/view_credits/credits.html", credits=credits, user=current_user)
    return redirect("/")

@student.route("/view-credits/sorted-by-credits-desc")
@login_required
def view_credits_sorted_by_credits_desc():
    role = current_user.role
    username = current_user.username
    if role == "student":
        credits = database.get_student_completed_courses_sorted_by(username, "credits", True)
        return render_template("student/tools/view_credits/credits_desc.html", credits=credits, user=current_user)
    return redirect("/")

@student.route("/view-credits/sorted-by-name")
@login_required
def view_credits_sorted_by_name():
    role = current_user.role
    username = current_user.username
    if role == "student":
        credits = database.get_student_completed_courses_sorted_by(username, "name", False)
        return render_template("student/tools/view_credits/name.html", credits=credits, user=current_user)
    return redirect("/")

@student.route("/view-credits/sorted-by-name-desc")
@login_required
def view_credits_sorted_by_name_desc():
    role = current_user.role
    username = current_user.username
    if role == "student":
        credits = database.get_student_completed_courses_sorted_by(username, "name", True)
        return render_template("student/tools/view_credits/name_desc.html", credits=credits, user=current_user)
    return redirect("/")

@student.route("/view-credits/sorted-by-key")
@login_required
def view_credits_sorted_by_key():
    role = current_user.role
    username = current_user.username
    if role == "student":
        credits = database.get_student_completed_courses_sorted_by(username, "key", False)
        return render_template("student/tools/view_credits/key.html", credits=credits, user=current_user)
    return redirect("/")

@student.route("/view-credits/sorted-by-key-desc")
@login_required
def view_credits_sorted_by_key_desc():
    role = current_user.role
    username = current_user.username
    if role == "student":
        credits = database.get_student_completed_courses_sorted_by(username, "key", True)
        return render_template("student/tools/view_credits/key_desc.html", credits=credits, user=current_user)
    return redirect("/")