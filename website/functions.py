from werkzeug.security import check_password_hash
import website.database as database
from string import ascii_letters



def login(username: str, password: str):
    real_password = database.get_password(username)
    if real_password is not None:
        if check_password_hash(real_password, password):
            return True
        return False
    return None


def new_password(password1: str, password2: str):
    if password1 == password2 and len(password1) >= 8:
        return True
    if password1 != password2 and len(password1) >= 8:
        return False
    return None


def new_username(username: str):
    check = database.search_username(username)
    if len(check) == 0:
        return True
    return False

def new_student(username: str):
    check = database.search_student(username)
    if len(check) == 0:
        return True
    return False

def username_valid(username: str):
    character_set = ascii_letters + "0123456789"
    for character in username:
        if character not in character_set:
            return False
    return True

def new_course_key(key: str):
    check = database.search_course_key(key)
    if len(check) == 0:
        return True
    return False

def new_role_request(username: str):
    check = database.search_user_role_request(username)
    if len(check) == 0:
        return True
    return False

def check_course_open(course_key: str):
    check = database.get_course_info(course_key)
    status = check[4]
    return status

def check_is_in_course(course_key: str, username: str):
    check = database.search_user_in_course(course_key, username)
    if len(check) > 0:
        return True
    return False