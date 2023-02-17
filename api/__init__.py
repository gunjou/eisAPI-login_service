from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

from api.endpoints import login_bp


api = Flask(__name__)
CORS(api)

api.config['JWT_SECRET_KEY'] = 'c06c5bbd202332b1ac34e7c0bd3ec660'
api.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)
jwt = JWTManager(api)

api.register_blueprint(login_bp)
