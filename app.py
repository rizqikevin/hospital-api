from flask import Flask
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # Import Flask-Migrate

# Inisialisasi app
app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi database dan JWT
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)  # Inisialisasi Migrate

# Import dan registrasi blueprint routes
from routes.auth_routes import auth_bp
from routes.employee_routes import employee_bp
from routes.doctor_routes import doctor_bp
from routes.patient_routes import patient_bp
from routes.appointment_routes import appointment_bp

app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(appointment_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
