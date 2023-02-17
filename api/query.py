from sqlalchemy import text

from api.config import get_connection

engine = get_connection()


def check_user(username): # Login
    result = engine.execute(
        text(f"""SELECT * FROM UsersAuth ua 
        JOIN RumahSakit_m rsm 
        ON rsm.id_rs = ua.id_rs 
        WHERE ua.username = '{username}';"""))
    return result

def get_data(public_id): # Profile
    result = engine.execute(
        text(f"""SELECT * FROM UsersAuth ua 
        JOIN RumahSakit_m rsm 
        ON rsm.id_rs = ua.id_rs 
        WHERE ua.public_id = '{public_id}';"""))
    return result
