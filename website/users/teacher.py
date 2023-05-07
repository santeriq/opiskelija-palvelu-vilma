from flask import Blueprint, redirect, render_template, flash, request, jsonify
from flask_login import login_required, current_user
import json
import website.database as database
import website.functions as functions

teacher = Blueprint("teacher", __name__)



@teacher.route("/join-course", methods=["GET", "POST"])
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

@teacher.route("/leave-course", methods=["GET", "POST"])
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


@teacher.route("/view-my-courses")
@login_required
def view_my_courses():
    role = current_user.role
    username = current_user.username
    if role == "admin" or role == "teacher" or role == "student":
        my_courses = database.get_user_courses(username)
        return render_template("teacher/tools/view_my_courses.html", courses_list=my_courses, user=current_user)
    return redirect("/")

@teacher.route("/manage-course", methods=["GET", "POST"])
@login_required
def manage_course(key):
    role = current_user.role
    students = database.get_course_students(key)
    if role == "admin" or role == "teacher":
        if request.method == "POST":
            username = request.form.get("username")
            confirm = request.form.get("remove")
            grade = request.form.get("grade")
            if username is not None:
                if functions.check_is_in_course(key, username) is False:
                    flash(f'"{username}" ei ole kurssilla', category="error")
                elif confirm == "POISTA":
                    database.remove_student_from_course(key, username)
                    flash(f'Poistettiin opiskelija "{username}" kurssilta', category="success")
                else:
                    database.update_student_grade(key, username, grade)
                    flash(f'Päivitettiin opiskelijan "{username}" arvosanaksi {grade}')
                students = database.get_course_students(key)
                return render_template("teacher/tools/manage_course.html", key=key, students_list=students, user=current_user)
        return render_template("teacher/tools/manage_course.html", key=key, students_list=students, user=current_user)
    return redirect("/")


