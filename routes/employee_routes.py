from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Employee
from datetime import datetime

employee_bp = Blueprint('employee_bp', __name__)

# GET All Employees
@employee_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    return jsonify({"status": "success", "data": [e.to_dict() for e in employees]}), 200

# GET Employee by ID
@employee_bp.route('/employees/<int:id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"status": "error", "message": "Employee tidak ditemukan"}), 404
    return jsonify({"status": "success", "data": emp.to_dict()}), 200

# CREATE Employee
@employee_bp.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    gender = data.get('gender')
    birthdate = data.get('birthdate')
    if Employee.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "Username sudah terdaftar"}), 400
    try:
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"status": "error", "message": "Format birthdate harus YYYY-MM-DD"}), 400
    new_emp = Employee(name, username, password, gender, birthdate_obj)
    db.session.add(new_emp)
    db.session.commit()
    return jsonify({"status": "success", "data": new_emp.to_dict()}), 201

# UPDATE Employee
@employee_bp.route('/employees/<int:id>', methods=['PUT'])
@jwt_required()
def update_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"status": "error", "message": "Employee tidak ditemukan"}), 404
    data = request.get_json()
    emp.name = data.get('name', emp.name)
    emp.username = data.get('username', emp.username)
    emp.gender = data.get('gender', emp.gender)
    birthdate = data.get('birthdate')
    if birthdate:
        try:
            emp.birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"status": "error", "message": "Format birthdate harus YYYY-MM-DD"}), 400
    db.session.commit()
    return jsonify({"status": "success", "data": emp.to_dict()}), 200

# DELETE Employee
@employee_bp.route('/employees/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"status": "error", "message": "Employee tidak ditemukan"}), 404
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"status": "success", "data": None}), 200
