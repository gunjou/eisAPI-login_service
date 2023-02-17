import json
from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, unset_jwt_cookies
from datetime import datetime, timezone, timedelta
from api.query import check_user, get_data

login_bp = Blueprint('login', __name__)


def get_current_user():
    current_user = get_data(get_jwt_identity()).fetchall()[0]
    return current_user

@login_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=1))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data['access_token'] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response

@login_bp.route('/users/login', methods=['POST'])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return {"message": "Wrong username or password"}, 401

    try:
        row = check_user(username).fetchall()[0]
    except:
        return {"message": "Wrong username or password"}, 401

    if check_password_hash(row['password'], password):
        access_token = create_access_token(identity=row['public_id'])

    return {
        "access_token": access_token,
        "current_user": {
            "id_data": row['id_rs'],
            "rs_name": row['display_name'],
            "rs_logo": row['logo_url'],
        }
    }

@login_bp.route('/users/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response

@login_bp.route('/users/profile')
@jwt_required()
def my_profile():
    # row = get_data(get_jwt_identity()).fetchall()[0]
    # print(row)
    current_user = get_current_user()
    result = {
        "username": current_user['username'],
        "email": current_user['email'],
        "id_rs": current_user['id_rs'],
        "nama_rs": current_user['nama_rs'],
        "alamat": current_user['alamat'],
    }

    return result
