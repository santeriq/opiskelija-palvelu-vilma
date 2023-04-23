from . import db
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text
from datetime import datetime

def create_user(username: str, password: str):
    password_hash = generate_password_hash(password)
    role = "none"
    visible = "true"
    sql = text("INSERT INTO users (username, password, role, visible) VALUES (:username, :password, :role, :visible)")
    db.session.execute(sql, {"username":username, "password":password_hash, "role":role, "visible":visible})
    db.session.commit()
    return f"created new user: {username}"

def create_course(key: str, name: str, credits: int):
    key = key.lower()
    open = "true"
    visible = "true"
    sql = text("INSERT INTO courses (tag, name, credits, open, visible) VALUES (:tag, :name, :credits, :open, :visible)")
    db.session.execute(sql, {"tag":key, "name":name, "credits":credits, "open":open, "visible":visible})
    db.session.commit()
    return f"created new course: {name} / {credits} / {key}"

def create_role_request(username: str, message: str):
    datetime_now = datetime.now()
    datetime_string = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
    if message == "" or message is None:
        message = "-"
    sql = text("INSERT INTO studentrolerequests (username, message, sent) VALUES (:username, :message, :sent)")
    db.session.execute(sql, {"username":username, "message":message, "sent":datetime_string})
    db.session.commit()
    return f"New role request created: {username} / {message} / {datetime_string}"

def update_role_request(username: str, message: str):
    if message == "" or message is None:
        message = "-"
    sql = text("UPDATE studentrolerequests SET message=:message WHERE username=:username")
    db.session.execute(sql, {"username":username, "message":message})
    db.session.commit()
    return f"Updated role request: {username} / {message}"

def update_course(key: str, name: str, credits: int, status: str):
    sql = text("UPDATE courses SET name=:name, credits=:credits, open=:status WHERE tag=:key AND visible=true")
    db.session.execute(sql, {"name":name, "credits":credits, "status":status, "key":key})
    db.session.commit()
    return f"Updated course: {name} / {credits} / {key} / {status}"

def set_user_role(username, role):
    sql = text("UPDATE users SET role=:role WHERE username=:username")
    db.session.execute(sql, {"username":username, "role":role})
    db.session.commit()
    return f'set "{username}" as {role}'

def get_password(username: str):
    username = username.lower()
    sql = text("SELECT password FROM users WHERE LOWER(username)=:username AND visible=true")
    data = db.session.execute(sql, {"username":username}).fetchone()
    if data is not None:
        return data[0]
    return None

def get_user_id(username: str):
    username = username.lower()
    sql = text("SELECT id FROM users WHERE LOWER(username)=:username AND visible=true")
    data = db.session.execute(sql, {"username":username}).fetchone()
    if data is not None:
        return data[0]
    return None

def get_courses_list_sorted_by_name():
    sql = text("SELECT name, tag, credits, open FROM courses WHERE visible=true ORDER BY name")
    data = db.session.execute(sql).fetchall()
    return data

def get_courses_list_sorted_by_key():
    sql = text("SELECT name, tag, credits, open FROM courses WHERE visible=true ORDER BY tag")
    data = db.session.execute(sql).fetchall()
    return data

def get_courses_list_sorted_by_credits():
    sql = text("SELECT name, tag, credits, open FROM courses WHERE visible=true ORDER BY credits DESC")
    data = db.session.execute(sql).fetchall()
    return data

def get_courses_list_sorted_by_open():
    sql = text("SELECT name, tag, credits, open FROM courses WHERE visible=true ORDER BY open DESC")
    data = db.session.execute(sql).fetchall()
    return data

def get_role_requests_list():
    sql = text("SELECT username, message, sent FROM studentrolerequests ORDER BY id")
    data = db.session.execute(sql).fetchall()
    return data

def search_user_role_request(username: str):
    username = username.lower()
    sql = text("SELECT message FROM studentrolerequests WHERE LOWER(username)=:username")
    data = db.session.execute(sql, {"username":username}).fetchall()
    return data

def search_username(username: str):
    username = username.lower()
    sql = text("SELECT username FROM users WHERE LOWER(username)=:username AND visible=true")
    data = db.session.execute(sql, {"username":username}).fetchall()
    return data

def search_course_key(key: str):
    key = key.lower()
    sql = text("SELECT tag FROM courses WHERE tag=:tag AND visible=true")
    data = db.session.execute(sql, {"tag":key}).fetchall()
    return data

def accept_role_request(username):
    sql = text("DELETE FROM studentrolerequests WHERE username=:username")
    db.session.execute(sql, {"username":username})
    db.session.commit()
    set_user_role(username, "student")
    return f"Accepted student request from {username}"


def reject_role_request(username):
    sql = text("DELETE FROM studentrolerequests WHERE username=:username")
    db.session.execute(sql, {"username":username})
    db.session.commit()
    return f"Delete student role request from {username}"