import os

class Config:
    # Gunakan environment variable atau fallback ke nilai default
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://rizqikevin:user123@localhost:5432/hospital_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecretkey')
    # Path ke kredensial BigQuery (disimpan dalam env)
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/delman-viewer-367ebe359fdf.json')
