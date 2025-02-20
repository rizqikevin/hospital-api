from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
from enum import Enum
from utils.auth_utils import hash_password, check_password

db = SQLAlchemy()

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Disimpan sebagai hashed password
    gender = db.Column(db.String(10), nullable=False)  # 'Male' atau 'Female'
    birthdate = db.Column(db.Date, nullable=False)

    def __init__(self, name, username, password, gender, birthdate):
        self.name = name
        self.username = username
        self.password = hash_password(password)
        self.gender = gender
        self.birthdate = birthdate

    def check_password(self, password):
        return check_password(password, self.password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "gender": self.gender,
            "birthdate": self.birthdate.strftime("%Y-%m-%d")
        }

# Doctor Model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    work_start_time = db.Column(db.Time, nullable=False)
    work_end_time = db.Column(db.Time, nullable=False)

    def __init__(self, name, username, password, work_start_time, work_end_time):
        self.name = name
        self.username = username
        self.password = hash_password(password)
        self.work_start_time = work_start_time
        self.work_end_time = work_end_time

    def check_password(self, password):
        return check_password(password, self.password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "work_start_time": self.work_start_time.strftime("%H:%M"),
            "work_end_time": self.work_end_time.strftime("%H:%M")
        }

# Patient Model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    no_ktp = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    vaccine_type = db.Column(db.String(50), nullable=True)
    vaccine_count = db.Column(db.Integer, nullable=True)

    def __init__(self, name, no_ktp, address):
        self.name = name
        self.no_ktp = no_ktp
        self.address = address

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "no_ktp": self.no_ktp,
            "address": self.address,
            "vaccine_type": self.vaccine_type,
            "vaccine_count": self.vaccine_count
        }

# Appointment Model
class AppointmentStatus(Enum):
    IN_QUEUE = "IN_QUEUE"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(AppointmentStatus), default=AppointmentStatus.IN_QUEUE, nullable=False)
    diagnose = db.Column(db.Text, default="", nullable=True)
    notes = db.Column(db.Text, default="", nullable=True)

    def __init__(self, patient_id, doctor_id, datetime, status=AppointmentStatus.IN_QUEUE):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.datetime = datetime
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M"),
            "status": self.status.value,
            "diagnose": self.diagnose,
            "notes": self.notes
        }
