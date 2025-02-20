from flask import Blueprint, request, jsonify
from models import Employee
from flask_jwt_extended import create_access_token
from models import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = Employee.query.filter_by(username=username).first()
    if not user:
        return jsonify({"status": "error", "message": "Username tidak terdaftar"}), 404
    if not user.check_password(password):
        return jsonify({"status": "error", "message": "Password salah"}), 401
    token = create_access_token(identity=user.username)
    return jsonify({"status": "success", "token": token}), 200
