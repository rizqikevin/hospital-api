# Hospital Management Backend

## Deskripsi
Sistem backend untuk dashboard manajemen rumah sakit, dengan fitur autentikasi, CRUD untuk Employee, Doctor, Patient, Appointment, dan sinkronisasi data pasien dari Google BigQuery.

## Stack
- Python 3.7
- Flask 2.0.1
- PostgreSQL 11
- SQLAlchemy
- Docker & Docker Compose
- JWT & bcrypt
- Google Cloud BigQuery

## Instalasi & Deployment
1. **Clone repository**:

2. **Atur Environment Variables**:
- `DATABASE_URL`: (Opsional, default sudah diatur di config.py)
- `JWT_SECRET_KEY`: Secret untuk JWT.
- `GOOGLE_APPLICATION_CREDENTIALS`: Path ke file kredensial BigQuery.

3. **Jalankan Docker Compose**:
    docker-compose up --build
Aplikasi akan berjalan di `http://localhost:5000`.

## API Endpoints

### Autentikasi
- **POST /login**
- Input: `{ "username": "admin", "password": "admin123" }`
- Response:
 ```json
 { "status": "success", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6..." }
 ```

### Employee
- **GET /employees**: Dapatkan semua employee.
- **POST /employees**: Buat employee baru.
- **GET /employees/:id**: Dapatkan detail employee.
- **PUT /employees/:id**: Update employee.
- **DELETE /employees/:id**: Hapus employee.

### Doctor
- **GET /doctors**, **POST /doctors**, **GET /doctors/:id**, **PUT /doctors/:id**, **DELETE /doctors/:id**
- Validasi work_start_time dan work_end_time.

### Patient
- **GET /patients**, **POST /patients**, **GET /patients/:id**, **PUT /patients/:id**, **DELETE /patients/:id**
- Validasi unik `no_ktp`.
- Data `vaccine_type` dan `vaccine_count` disinkronisasi dari BigQuery.

### Appointment
- **GET /appointments**, **POST /appointments**, **GET /appointments/:id**, **PUT /appointments/:id**, **DELETE /appointments/:id**
- Validasi waktu appointment dalam jam kerja dokter dan tidak ada konflik jadwal.
- Status: IN_QUEUE, DONE, CANCELLED.

## Testing
Untuk menjalankan unit testing:
pytest

---
