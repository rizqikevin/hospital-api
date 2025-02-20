from google.cloud import bigquery
from models import db, Patient
import os

def sync_patients():
    client = bigquery.Client()
    query = """
        SELECT no_ktp, vaccine_type, vaccine_count 
        FROM `delman-internal.delman_interview.vaccine_data`
    """
    results = client.query(query).result()
    for row in results:
        patient = Patient.query.filter_by(no_ktp=row.no_ktp).first()
        if patient:
            patient.vaccine_type = row.vaccine_type
            patient.vaccine_count = row.vaccine_count
    db.session.commit()
