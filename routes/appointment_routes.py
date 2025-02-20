from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Appointment, Patient, Doctor, AppointmentStatus
from datetime import datetime

appointment_bp = Blueprint('appointment_bp', __name__)

# GET All Appointments
@appointment_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify({"status": "success", "data": [a.to_dict() for a in appointments]}), 200

# GET Appointment by ID
@appointment_bp.route('/appointments/<int:id>', methods=['GET'])
@jwt_required()
def get_appointment(id):
    appo = Appointment.query.get(id)
    if not appo:
        return jsonify({"status": "error", "message": "Appointment tidak ditemukan"}), 404
    return jsonify({"status": "success", "data": appo.to_dict()}), 200

# CREATE Appointment
@appointment_bp.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    dt_str = data.get('datetime')
    try:
        appt_datetime = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"status": "error", "message": "Format datetime harus YYYY-MM-DD HH:MM"}), 400

    patient = Patient.query.get(patient_id)
    doctor = Doctor.query.get(doctor_id)
    if not patient:
        return jsonify({"status": "error", "message": "Patient tidak ditemukan"}), 404
    if not doctor:
        return jsonify({"status": "error", "message": "Doctor tidak ditemukan"}), 404

    # Validasi: Waktu appointment harus dalam jam kerja dokter
    if not (doctor.work_start_time <= appt_datetime.time() <= doctor.work_end_time):
        return jsonify({"status": "error", "message": "Waktu appointment di luar jam kerja dokter"}), 400

    # Validasi: Tidak ada konflik jadwal dokter
    conflict = Appointment.query.filter_by(doctor_id=doctor_id, datetime=appt_datetime).first()
    if conflict:
        return jsonify({"status": "error", "message": "Doctor sudah memiliki appointment pada waktu tersebut"}), 400

    new_app = Appointment(patient_id, doctor_id, appt_datetime, AppointmentStatus.IN_QUEUE)
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"status": "success", "data": new_app.to_dict()}), 201

# UPDATE Appointment
@appointment_bp.route('/appointments/<int:id>', methods=['PUT'])
@jwt_required()
def update_appointment(id):
    appo = Appointment.query.get(id)
    if not appo:
        return jsonify({"status": "error", "message": "Appointment tidak ditemukan"}), 404
    data = request.get_json()
    # Hanya izinkan update diagnose, notes, dan status (misalnya oleh dokter)
    status = data.get('status')
    if status and status in [s.value for s in AppointmentStatus]:
        appo.status = AppointmentStatus(status)
    appo.diagnose = data.get('diagnose', appo.diagnose)
    appo.notes = data.get('notes', appo.notes)
    db.session.commit()
    return jsonify({"status": "success", "data": appo.to_dict()}), 200

# DELETE Appointment
@appointment_bp.route('/appointments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(id):
    appo = Appointment.query.get(id)
    if not appo:
        return jsonify({"status": "error", "message": "Appointment tidak ditemukan"}), 404
    db.session.delete(appo)
    db.session.commit()
    return jsonify({"status": "success", "data": None}), 200
