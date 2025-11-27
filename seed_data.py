from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models.models import Base, User, Patient, Appointment, Request, UserType, AppointmentStatus, RequestStatus, RefreshToken
from utils import get_password_hash
from datetime import date, datetime, timedelta
import json

# Cria as tabelas
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    try:
        # Limpa dados existentes
        db.query(Request).delete()
        db.query(Appointment).delete()
        db.query(Patient).delete()
        db.query(User).delete()
        db.commit()

        # Cria usuários (psicólogos e pacientes)
        users_data = [
            {
                "id": 1,
                "email": "psicologo.2025@outlook.com",
                "password": get_password_hash("123456"),
                "type": UserType.PSICOLOGO,
                "name": "psicologo teste",
                "specialty": "TCC",
                "crp": "01123456",
                "phone": "35999082544"
            },
            {
                "id": 2,
                "email": "ana@test.com",
                "password": get_password_hash("123456"),
                "type": UserType.PSICOLOGO,
                "name": "Dra. Ana Costa",
                "specialty": "Terapia Cognitivo-Comportamental",
                "crp": "CRP 01/23456"
            }
        ]

        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
        db.commit()

        # Cria pacientes
        patients_data = [
            {
                "id": 1,
                "name": "paciente teste",
                "email": "paciente.2025@outlook.com",
                "phone": "035998758544",
                "birth_date": date(1985, 11, 26),
                "age": 39,
                "status": "Ativo",
                "psychologist_id": 1
            },
            {
                "id": 2,
                "name": "Segundo Paciente",
                "email": "paciente2@test.com",
                "phone": "(11) 99999-2222",
                "birth_date": date(1990, 1, 1),
                "age": 34,
                "status": "Ativo",
                "psychologist_id": 1
            }
        ]

        for patient_data in patients_data:
            patient = Patient(**patient_data)
            db.add(patient)
        db.commit()

        print("✅ Dados de teste inseridos com sucesso!")
        print("👨‍⚕️ Psicólogo: psicologo.2025@outlook.com / 123456")
        print("🧑‍🦱 Paciente 1: paciente.2025@outlook.com")
        print("🧑‍🦱 Paciente 2: paciente2@test.com")

    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()