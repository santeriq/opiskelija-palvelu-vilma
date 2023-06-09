from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import getenv


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    db.init_app(app)

    from .routes import routes
    from .auth import auth
    from .users import admin
    from .users import teacher
    from .users import student

    app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(admin.admin, url_prefix="/admin")
    app.register_blueprint(teacher.teacher, url_prefix="/teacher")
    app.register_blueprint(student.student, url_prefix="/student")


    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from website.models import User
    import website.database as database

    @login_manager.user_loader
    def load_user(id):
        return User(id)

    return app
