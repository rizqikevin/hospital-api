from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Patient

patient_bp = Blueprint('patient_bp', __name__)

# GET All Patients
@patient_bp.route('/patients', methods=['GET'])
@jwt_required()
def get_patients():
    patients = Patient.query.all()
    return jsonify({"status": "success", "data": [p.to_dict() for p in patients]}), 200

# GET Patient by ID
@patient_bp.route('/patients/<int:id>', methods=['GET'])
@jwt_required()
def get_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"status": "error", "message": "Patient tidak ditemukan"}), 404
    return jsonify({"status": "success", "data": patient.to_dict()}), 200

# CREATE Patient
@patient_bp.route('/patients', methods=['POST'])
@jwt_required()
def create_patient():
    data = request.get_json()
    name = data.get('name')
    no_ktp = data.get('no_ktp')
    address = data.get('address')
    if Patient.query.filter_by(no_ktp=no_ktp).first():
        return jsonify({"status": "error", "message": "Patient dengan no_ktp ini sudah terdaftar"}), 400
    new_patient = Patient(name, no_ktp, address)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"status": "success", "data": new_patient.to_dict()}), 201

# UPDATE Patient
@patient_bp.route('/patients/<int:id>', methods=['PUT'])
@jwt_required()
def update_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"status": "error", "message": "Patient tidak ditemukan"}), 404
    data = request.get_json()
    patient.name = data.get('name', patient.name)
    patient.address = data.get('address', patient.address)
    db.session.commit()
    return jsonify({"status": "success", "data": patient.to_dict()}), 200

# DELETE Patient
@patient_bp.route('/patients/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"status": "error", "message": "Patient tidak ditemukan"}), 404
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"status": "success", "data": None}), 200
