from . import db
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text
from datetime import datetime
import website.functions as functions

def create_user(username: str, password: str):
    password_hash = generate_password_hash(password)
    role = "none"
    visible = "true"
    sql = text('INSERT INTO "Users" (username, password, role, visible) VALUES (:username, :password, :role, :visible)')
    db.session.execute(sql, {"username":username, "password":password_hash, "role":role, "visible":visible})
    db.session.commit()
    return f"created new user: {username}"

def create_course(key: str, name: str, credits: int):
    key = key.lower()
    open = "true"
    visible = "true"
    sql = text('INSERT INTO "Courses" (tag, name, credits, open, visible) VALUES (:tag, :name, :credits, :open, :visible)')
    db.session.execute(sql, {"tag":key, "name":name, "credits":credits, "open":open, "visible":visible})
    db.session.commit()
    return f"created new course: {name} / {credits} / {key}"

def create_role_request(username: str, message: str):
    datetime_now = datetime.now()
    datetime_string = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
    if message == "" or message is None:
        message = "-"
    sql = text('INSERT INTO "RoleRequests" (username, message, sent) VALUES (:username, :message, :sent)')
    db.session.execute(sql, {"username":username, "message":message, "sent":datetime_string})
    db.session.commit()
    return f"New role request created: {username} / {message} / {datetime_string}"

def update_role_request(username: str, message: str):
    if message == "" or message is None:
        message = "-"
    sql = text('UPDATE "RoleRequests" SET message=:message WHERE username=:username')
    db.session.execute(sql, {"username":username, "message":message})
    db.session.commit()
    return f"Updated role request: {username} / {message}"

def update_course(key: str, name: str, credits: int, status: str):
    sql = text("UPDATE courses SET name=:name, credits=:credits, open=:status WHERE tag=:key AND visible=true")
    db.session.execute(sql, {"name":name, "credits":credits, "status":status, "key":key})
    db.session.commit()
    return f"Updated course: {name} / {credits} / {key} / {status}"

def set_user_role(username: str, role: str):
    username.lower()
    role.lower()
    sql = text('UPDATE "Users" SET role=:role WHERE LOWER(username)=:username')
    db.session.execute(sql, {"username":username, "role":role})
    db.session.commit()
    return f'set "{username}" as {role}'

def get_password(username: str):
    username = username.lower()
    sql = text('SELECT password FROM "Users" WHERE LOWER(username)=:username AND visible=true')
    data = db.session.execute(sql, {"username":username}).fetchone()
    if data is not None:
        return data[0]
    return None

def get_user_id(username: str):
    username = username.lower()
    sql = text('SELECT id FROM "Users" WHERE LOWER(username)=:username AND visible=true')
    data = db.session.execute(sql, {"username":username}).fetchone()
    if data is not None:
        return data[0]
    return None

def get_users_list_sorted_by(column: str, desc: bool=False):
    column.lower()
    sql = "-"
    if column == "id" and desc is False:
        sql = text('SELECT id, username, role FROM "Users" WHERE visible=true ORDER BY id')
    elif column == "id" and desc is True:
        sql = text('SELECT id, username, role FROM "Users" WHERE visible=true ORDER BY id DESC')
    elif column == "username" and desc is False:
        sql = text('SELECT id, username, role FROM "Users" WHERE visible=true ORDER BY username')
    elif column == "username" and desc is True:
        sql = text('SELECT id, username, role FROM "Users" WHERE visible=true ORDER BY username DESC')
    if sql != "-":
        data = db.session.execute(sql).fetchall()
        return data
    return "Invalid parameter input"

def get_courses_list_sorted_by(column: str, desc: bool=False):
    column.lower()
    sql = "-"
    if column == "name" and desc is False:
        sql = text('SELECT name, tag, credits, open FROM "Courses" WHERE visible=true ORDER BY name')
    elif column == "name" and desc is True:
        sql = text('SELECT name, tag, credits, open FROM "Courses" WHERE visible=true ORDER BY name DESC')
    elif column == "key" and desc is False:
        sql = text('SELECT name, tag, credits, open FROM "Courses" WHERE visible=true ORDER BY tag')
    elif column == "key" and desc is True:
        sql = text('SELECT name, tag, credits, open FROM "Courses" WHERE visible=true ORDER BY tag DESC')
    elif column == "credits" and desc is False:
        sql = text('SELECT name, tag, credits, open FROM "Courses" WHERE visible=true ORDER BY credits')
    elif column == "credits" and desc is True:
        sql = text('SELECT name, tag, credits, open FROM "Courses" WHERE visible=true ORDER BY credits DESC')
    elif column == "open" and desc is False:
        sql = text('SELECT name, tag, credits, open FROM "Courses" WHERE visible=true ORDER BY open')
    elif column == "open" and desc is True:
        sql = text('SELECT name, tag, credits, open FROM "Courses" WHERE visible=true ORDER BY open DESC')
    if sql != "-":
        data = db.session.execute(sql).fetchall()
        return data
    return "Invalid parameter input"


def get_role_requests_list():
    sql = text('SELECT username, message, sent FROM "RoleRequests" ORDER BY id')
    data = db.session.execute(sql).fetchall()
    return data

def search_user_role_request(username: str):
    username = username.lower()
    sql = text('SELECT message FROM "RoleRequests" WHERE LOWER(username)=:username')
    data = db.session.execute(sql, {"username":username}).fetchall()
    return data

def search_username(username: str):
    username = username.lower()
    sql = text('SELECT username FROM "Users" WHERE LOWER(username)=:username AND visible=true')
    data = db.session.execute(sql, {"username":username}).fetchall()
    return data

def search_course_key(key: str):
    key = key.lower()
    sql = text('SELECT tag FROM "Courses" WHERE tag=:tag AND visible=true')
    data = db.session.execute(sql, {"tag":key}).fetchall()
    return data

def accept_role_request(username):
    sql = text('DELETE FROM "RoleRequests" WHERE username=:username')
    db.session.execute(sql, {"username":username})
    db.session.commit()
    set_user_role(username, "student")
    return f"Accepted student request from {username}"


def reject_role_request(username):
    sql = text('DELETE FROM "RoleRequests" WHERE username=:username')
    db.session.execute(sql, {"username":username})
    db.session.commit()
    return f"Delete student role request from {username}"

def delete_user(username: str):
    username.lower()
    if functions.new_role_request(username) is False:
        reject_role_request(username)
    sql = text('UPDATE "Users" SET visible=false WHERE LOWER(username)=:username AND visible=true')
    db.session.execute(sql, {"username":username})
    db.session.commit()
    return f"Deleted user {username}"