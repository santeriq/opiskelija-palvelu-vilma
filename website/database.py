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

def create_student(username: str):
    username.lower()
    credits = 0
    visible = "true"
    sql = text('INSERT INTO "Students" (username, credits, visible) VALUES (:username, :credits, :visible)')
    db.session.execute(sql, {"username":username, "credits":credits, "visible":visible})
    db.session.commit()
    return f"Created new student: {username}"

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
    username = username.lower()
    if message == "" or message is None:
        message = "-"
    sql = text('UPDATE "RoleRequests" SET message=:message WHERE username=:username')
    db.session.execute(sql, {"username":username, "message":message})
    db.session.commit()
    return f"Updated role request: {username} / {message}"

def update_course(key: str, name: str, credits: int, status: str):
    key = key.lower()
    name = name.lower()
    status = status.lower()
    sql = text('UPDATE "Courses" SET name=:name, credits=:credits, open=:status WHERE tag=:key AND visible=true')
    db.session.execute(sql, {"name":name, "credits":credits, "status":status, "key":key})
    db.session.commit()
    return f"Updated course: {name} / {credits} / {key} / {status}"

def update_student_credits(username: str, credits: int):
    username = username.lower()
    old_credits = get_student_credits(username)
    new_credits = old_credits + credits
    sql = text('UPDATE "Students" SET credits=:new_credits WHERE visible=true')
    db.session.execute(sql, {"username":username, "new_credits":new_credits})
    db.session.commit()
    return f"Updated student {username} credits from {old_credits} to {new_credits}"

def set_user_role(username: str, role: str):
    old_role = get_user_role(username)
    username.lower()
    role.lower()
    if role == "student" and old_role != "student":
        create_student(username)
    elif role != "student" and old_role == "student":
        delete_student(username)
    sql = text('UPDATE "Users" SET role=:role WHERE LOWER(username)=:username')
    db.session.execute(sql, {"username":username, "role":role})
    db.session.commit()
    return f'Set "{username}" as {role}'

def get_password(username: str):
    username = username.lower()
    sql = text('SELECT password FROM "Users" WHERE LOWER(username)=:username AND visible=true')
    data = db.session.execute(sql, {"username":username}).fetchone()
    if data is not None:
        return data[0]
    return None

def get_user_id(username: str):
    username.lower()
    sql = text('SELECT id FROM "Users" WHERE LOWER(username)=:username AND visible=true')
    data = db.session.execute(sql, {"username":username}).fetchone()
    if data is not None:
        return data[0]
    return None

def get_user_role(username: str):
    username.lower()
    sql = text('SELECT role FROM "Users" WHERE LOWER(username)=:username AND visible=true')
    data = db.session.execute(sql, {"username":username}).fetchone()
    if data is not None:
        return data[0]
    return None

def get_student_credits(username: str):
    username = username.lower()
    sql = text('SELECT credits FROM "Students" WHERE LOWER(username)=:username AND visible=true')
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

def get_students_list_sorted_by(column: str, desc: bool=False):
    column.lower()
    sql = "-"
    if column == "id" and desc is False:
        sql = text('SELECT * FROM "Students" WHERE visible=true ORDER BY id')
    elif column == "id" and desc is True:
        sql = text('SELECT * FROM "Students" WHERE visible=true ORDER BY id DESC')
    elif column == "username" and desc is False:
        sql = text('SELECT * FROM "Students" WHERE visible=true ORDER BY username')
    elif column == "username" and desc is True:
        sql = text('SELECT * FROM "Students" WHERE visible=true ORDER BY username DESC')
    elif column == "credits" and desc is False:
        sql = text('SELECT * FROM "Students" WHERE visible=true ORDER BY credits')
    elif column == "credits" and desc is True:
        sql = text('SELECT * FROM "Students" WHERE visible=true ORDER BY credits DESC')
    if sql != "-":
        data = db.session.execute(sql).fetchall()
        return data
    return "Invalid parameter input"

def get_course_info(key: str):
    key = key.lower()
    sql = text('SELECT * FROM "Courses" WHERE tag=:tag AND visible=true')
    data = db.session.execute(sql, {"tag":key}).fetchone()
    return data

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

def search_student(username: str):
    username = username.lower()
    sql = text('SELECT username FROM "Students" WHERE LOWER(username)=:username AND visible=true')
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
    txt = ""
    username = username.lower()
    role = get_user_role(username)
    if functions.new_role_request(username) is False:
        reject_role_request(username)
    if role == "student":
        delete_student(username)
        txt = ", also removed from students list"
    sql = text('UPDATE "Users" SET visible=false WHERE LOWER(username)=:username AND visible=true')
    db.session.execute(sql, {"username":username})
    db.session.commit()
    return f"Deleted user {username}" + txt

def delete_student(username: str):
    username.lower()
    sql = text('UPDATE "Students" SET visible=false WHERE LOWER(username)=:username AND visible=true')
    db.session.execute(sql, {"username":username})
    db.session.commit()
    return f"Deleted student: {username}"


def search_user_in_course(key: str, username: str):
    key.lower()
    username.lower()
    sql = text('SELECT * FROM "InCourse" WHERE course_tag=:key AND username=:username')
    data = db.session.execute(sql, {"key":key, "username":username}).fetchall()
    return data

def join_course(key: str, username: str):
    key.lower()
    username.lower()
    course_id = get_course_info(key)[0]
    user_id = get_user_id(username)
    grade = 0
    sql = text('INSERT INTO "InCourse" (course_id, course_tag, user_id, username, grade) VALUES (:course_id, :course_tag, :user_id, :username, :grade)')
    db.session.execute(sql, {"course_id":course_id, "course_tag":key, "user_id":user_id, "username":username, "grade":grade})
    db.session.commit()
    return f"{username} joined the course {key}"

def leave_course(key: str, username: str):
    key.lower()
    username.lower()
    sql = text('DELETE FROM "InCourse" WHERE course_tag=:course_tag AND username=:username')
    db.session.execute(sql, {"course_tag":key, "username":username})
    db.session.commit()
    return f"{username} left the course {key}"

def get_user_courses(username: str):
    username.lower()
    sql = text('SELECT "Courses".name, "Courses".credits, "Courses".tag FROM "Courses", "InCourse" WHERE "Courses".tag="InCourse".course_tag AND "Courses".visible=true AND "InCourse".username=:username')
    data = db.session.execute(sql, {"username":username}).fetchall()
    return data

def get_course_students(key: str):
    key.lower()
    sql = text('SELECT "InCourse".username, "InCourse".grade FROM "InCourse", "Students" WHERE "InCourse".course_tag=:course_tag AND "InCourse".username="Students".username')
    data = db.session.execute(sql, {"course_tag":key}).fetchall()
    return data

def update_student_grade(key: str, username: str, grade: int):
    key.lower()
    username.lower()
    credits = int(get_course_credits(key))
    old_credits = int(get_student_credits(username))
    new_credits = old_credits + credits
    sql = text('UPDATE "InCourse" SET grade=:grade WHERE course_tag=:course_tag AND username=:username')
    db.session.execute(sql, {"course_tag":key, "username":username, "grade":grade})
    sql = text('UPDATE "Students" SET credits=:credits WHERE username=:username AND visible=true')
    db.session.execute(sql, {"credits":new_credits, "username":username})
    db.session.commit()
    return f'Updated {username} grade to {grade}'

def get_course_credits(key: str):
    key.lower()
    sql = text('SELECT credits FROM "Courses" WHERE tag=:course_tag AND visible=true')
    data = db.session.execute(sql, {"course_tag":key}).fetchone()
    if data is None:
        return None
    return data[0]

def remove_student_from_course(key: str, username: str):
    key.lower()
    username.lower()
    sql = text('DELETE FROM "InCourse" WHERE course_tag=:course_tag AND username=:username')
    db.session.execute(sql, {"course_tag":key, "username":username})
    db.session.commit()
    return f'Removed {username} from course "{key}"'


def get_student_gpa(username: str):
    username.lower()
    sql = text('SELECT SUM(grade) FROM "InCourse" WHERE username=:username')
    sum = db.session.execute(sql, {"username":username}).fetchone()
    sql = text('SELECT COUNT(grade) FROM "InCourse" WHERE username=:username AND grade>0')
    count = db.session.execute(sql, {"username":username}).fetchone()
    if sum is None or count is None:
        return None
    gpa = sum[0] / count[0]
    return gpa


def get_student_credits(username: str):
    username.lower()
    sql = text('SELECT credits FROM "Students" WHERE username=:username')
    data = db.session.execute(sql, {"username":username}).fetchone()
    return data[0]

def get_student_completed_courses_sorted_by(username: str, column: str, desc: bool=False):
    username.lower()
    sql = "-"
    if column == "name" and desc is False:
        sql = text('SELECT "Courses".name, "Courses".credits, "Courses".tag, "InCourse".grade FROM "Courses", "InCourse" WHERE "Courses".tag="InCourse".course_tag AND "InCourse".username=:username ORDER BY "Courses".name')
    elif column == "name" and desc is True:
        sql = text('SELECT "Courses".name, "Courses".credits, "Courses".tag, "InCourse".grade FROM "Courses", "InCourse" WHERE "Courses".tag="InCourse".course_tag AND "InCourse".username=:username ORDER BY "Courses".name DESC')
    elif column == "key" and desc is False:
        sql = text('SELECT "Courses".name, "Courses".credits, "Courses".tag, "InCourse".grade FROM "Courses", "InCourse" WHERE "Courses".tag="InCourse".course_tag AND "InCourse".username=:username ORDER BY "Courses".tag')
    elif column == "key" and desc is True:
        sql = text('SELECT "Courses".name, "Courses".credits, "Courses".tag, "InCourse".grade FROM "Courses", "InCourse" WHERE "Courses".tag="InCourse".course_tag AND "InCourse".username=:username ORDER BY "Courses".tag DESC')
    elif column == "credits" and desc is False:
        sql = text('SELECT "Courses".name, "Courses".credits, "Courses".tag, "InCourse".grade FROM "Courses", "InCourse" WHERE "Courses".tag="InCourse".course_tag AND "InCourse".username=:username ORDER BY "Courses".credits')
    elif column == "credits" and desc is True:
        sql = text('SELECT "Courses".name, "Courses".credits, "Courses".tag, "InCourse".grade FROM "Courses", "InCourse" WHERE "Courses".tag="InCourse".course_tag AND "InCourse".username=:username ORDER BY "Courses".credits DESC')
    elif column == "grade" and desc is False:
        sql = text('SELECT "Courses".name, "Courses".credits, "Courses".tag, "InCourse".grade FROM "Courses", "InCourse" WHERE "Courses".tag="InCourse".course_tag AND "InCourse".username=:username ORDER BY "InCourse".grade')
    elif column == "grade" and desc is True:
        sql = text('SELECT "Courses".name, "Courses".credits, "Courses".tag, "InCourse".grade FROM "Courses", "InCourse" WHERE "Courses".tag="InCourse".course_tag AND "InCourse".username=:username ORDER BY "InCourse".grade DESC')
    if sql == "-":
        return None
    data = db.session.execute(sql, {"username":username}).fetchall()
    return data
