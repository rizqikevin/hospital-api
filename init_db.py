from app import app, db
from models import Employee
from datetime import datetime

with app.app_context():
    db.create_all()  # Membuat semua tabel jika belum ada
    if not Employee.query.filter_by(username="admin").first():
        admin = Employee("Admin", "admin", "admin123", "Male", datetime.strptime("1990-01-01", "%Y-%m-%d").date())
        db.session.add(admin)
        db.session.commit()
        print("User admin berhasil ditambahkan!")
