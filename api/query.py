from sqlalchemy import text

from api.config import get_connection

engine = get_connection()


def get_id():  # Login
    result = engine.execute(
        text(f"""SELECT MAX(id) FROM UsersAuth;"""))
    return result


def check_user(username):  # Login
    result = engine.execute(
        text(f"""SELECT * FROM UsersAuth
            WHERE username = '{username}';"""))
    return result


def add_user(user_id, public_id, email, username, password, is_super):  # Sign up
    result = engine.execute(
        text(f"""INSERT INTO UsersAuth 
            VALUES ({user_id}, '{public_id}', '{email}', '{username}', '{password}', {is_super});"""))
    return result
