import uuid
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash

from api.config import SECRET_KEY
from api.query import *

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST'])
def login_user():
    auth_username = request.form.get('username')
    auth_password = request.form.get('password')
    if not auth_username or not auth_password:
        return make_response('could not verify', 401, {'Authentication': '"login required"'})

    row = check_user(auth_username).fetchall()[0]

    if check_password_hash(row['password'], auth_password):
        token = jwt.encode({'public_id': row['public_id'],
                            'exp': datetime.utcnow() + timedelta(minutes=15)},
                           SECRET_KEY, "HS256")
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})


@login_bp.route('/register', methods=['POST'])
def signup_user():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    user_id = get_id().scalar()
    public_id = str(uuid.uuid4())
    hashed_password = generate_password_hash(password, method='sha256')

    try:
        add_user(user_id+1, public_id, email, username, hashed_password, 0)
        return jsonify({'message': 'registered successfully'})
    except:
        return make_response('register failed', 400, {'message': 'register failed'})
