from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import login_user, login_required, logout_user, current_user
from website.models import User
import website.functions as functions
import website.database as database
import secrets

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        check = functions.login(username, password)
        user = User(database.get_user_id(username))
        if functions.new_username(username):
            flash("Käyttäjätunnusta ei löytynyt", category="error")
        elif not check:
            flash("Väärä salasana", category="error")
        elif check:
            login_user(user, remember=True)
            session["csrf_token"] = secrets.token_hex(16)
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


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
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
            database.create_user(username, password1)
            user = User(database.get_user_id(username))
            login_user(user, remember=True)
            return redirect(url_for("routes.guest"))
    return render_template("sign_up.html", user=current_user)
