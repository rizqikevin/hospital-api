from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Doctor
from datetime import datetime

doctor_bp = Blueprint('doctor_bp', __name__)

# GET All Doctors
@doctor_bp.route('/doctors', methods=['GET'])
@jwt_required()
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify({"status": "success", "data": [d.to_dict() for d in doctors]}), 200

# GET Doctor by ID
@doctor_bp.route('/doctors/<int:id>', methods=['GET'])
@jwt_required()
def get_doctor(id):
    doc = Doctor.query.get(id)
    if not doc:
        return jsonify({"status": "error", "message": "Doctor tidak ditemukan"}), 404
    return jsonify({"status": "success", "data": doc.to_dict()}), 200

# CREATE Doctor
@doctor_bp.route('/doctors', methods=['POST'])
@jwt_required()
def create_doctor():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    work_start_time = data.get('work_start_time')
    work_end_time = data.get('work_end_time')
    if Doctor.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "Username sudah terdaftar"}), 400
    try:
        ws = datetime.strptime(work_start_time, "%H:%M").time()
        we = datetime.strptime(work_end_time, "%H:%M").time()
    except ValueError:
        return jsonify({"status": "error", "message": "Format waktu harus HH:MM"}), 400
    new_doc = Doctor(name, username, password, ws, we)
    db.session.add(new_doc)
    db.session.commit()
    return jsonify({"status": "success", "data": new_doc.to_dict()}), 201

# UPDATE Doctor
@doctor_bp.route('/doctors/<int:id>', methods=['PUT'])
@jwt_required()
def update_doctor(id):
    doc = Doctor.query.get(id)
    if not doc:
        return jsonify({"status": "error", "message": "Doctor tidak ditemukan"}), 404
    data = request.get_json()
    doc.name = data.get('name', doc.name)
    doc.username = data.get('username', doc.username)
    ws = data.get('work_start_time')
    we = data.get('work_end_time')
    if ws and we:
        try:
            doc.work_start_time = datetime.strptime(ws, "%H:%M").time()
            doc.work_end_time = datetime.strptime(we, "%H:%M").time()
        except ValueError:
            return jsonify({"status": "error", "message": "Format waktu harus HH:MM"}), 400
    db.session.commit()
    return jsonify({"status": "success", "data": doc.to_dict()}), 200

# DELETE Doctor
@doctor_bp.route('/doctors/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_doctor(id):
    doc = Doctor.query.get(id)
    if not doc:
        return jsonify({"status": "error", "message": "Doctor tidak ditemukan"}), 404
    db.session.delete(doc)
    db.session.commit()
    return jsonify({"status": "success", "data": None}), 200
