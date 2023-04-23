from time import sleep
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from website.models import User
import website.functions as functions
import website.database as database

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        check = functions.login(username, password)
        username_not_exist = functions.new_username(username)
        user = User(database.get_user_id(username))
        if username_not_exist:
            flash("Käyttäjätunnusta ei löytynyt", category="error")
        elif check is False:
            flash("Väärä salasana", category="error")
        elif check is True:
            sleep(0.5)
            login_user(user, remember=True)
            if user.role == "admin":
                return redirect(url_for("routes.admin"))
            elif user.role == "teacher":
                return redirect(url_for("routes.teacher"))
            elif user.role == "student":
                return redirect(url_for("routes.student"))
            elif user.role == "none":
                return redirect(url_for("routes.guest"))
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User(database.get_user_id(username))
        if not functions.new_username(username):
            flash("Käyttäjätunnus ei ole vapaa", category="error")
        elif not functions.username_valid(username):
            flash("Käyttäjätunnus tulee koostua aakkosista ja numeroista", category="error")
        elif len(username) < 3:
            flash("Käyttäjätunnuksen tulee olla vähintään 3 merkkiä pitkä", category="error")
        elif len(username) > 18:
            flash("Käyttäjätunnuksen tulee olla 18 merkkiä tai vähemmän", category="error")
        elif password1 != password2:
            flash("Salasanat eivät täsmää", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters", category="error")
        else:
            flash("Käyttäjätunnus luotu", category="success")
            sleep(0.5)
            login_user(user, remember=True)
            database.create_user(username, password1)
            return redirect(url_for("routes.guest"))
    return render_template("sign_up.html", user=current_user)