from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from core.database import get_db
from models.models import User, Patient, Appointment, AppointmentStatus, UserType
from schemas.advanced_schemas import DashboardPsychologist, DashboardPatient, DashboardStats
from services.auth_service import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/psychologist", response_model=DashboardPsychologist)
async def get_psychologist_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Estatísticas
    total_patients = db.query(Patient).filter(Patient.psychologist_id == current_user.id).count()
    active_patients = db.query(Patient).filter(
        Patient.psychologist_id == current_user.id,
        Patient.status == "ativo"
    ).count()
    
    total_sessions = db.query(Appointment).filter(
        Appointment.psychologist_id == current_user.id
    ).count()
    
    upcoming_sessions = db.query(Appointment).filter(
        Appointment.psychologist_id == current_user.id,
        Appointment.status == AppointmentStatus.AGENDADO,
        Appointment.date >= datetime.now().date()
    ).count()
    
    # Sessões do mês atual
    first_day = datetime.now().replace(day=1)
    completed_this_month = db.query(Appointment).filter(
        Appointment.psychologist_id == current_user.id,
        Appointment.status == AppointmentStatus.CONCLUIDO,
        Appointment.date >= first_day.date()
    ).count()
    
    canceled_this_month = db.query(Appointment).filter(
        Appointment.psychologist_id == current_user.id,
        Appointment.status == AppointmentStatus.CANCELADO,
        Appointment.date >= first_day.date()
    ).count()
    
    # Taxa de comparecimento
    total_scheduled = completed_this_month + canceled_this_month
    attendance_rate = (completed_this_month / total_scheduled * 100) if total_scheduled > 0 else 0
    
    stats = DashboardStats(
        total_patients=total_patients,
        active_patients=active_patients,
        total_sessions=total_sessions,
        upcoming_sessions=upcoming_sessions,
        completed_this_month=completed_this_month,
        canceled_this_month=canceled_this_month,
        attendance_rate=round(attendance_rate, 2)
    )
    
    # Próximos agendamentos
    upcoming_appointments = db.query(Appointment).filter(
        Appointment.psychologist_id == current_user.id,
        Appointment.date >= datetime.now().date()
    ).order_by(Appointment.date, Appointment.time).limit(5).all()
    
    # Pacientes recentes
    recent_patients = db.query(Patient).filter(
        Patient.psychologist_id == current_user.id
    ).order_by(Patient.created_at.desc()).limit(5).all()
    
    # Alertas
    alerts = []
    high_risk_patients = db.query(Patient).filter(
        Patient.psychologist_id == current_user.id,
        Patient.risk_level == "alto"
    ).count()
    
    if high_risk_patients > 0:
        alerts.append({
            "type": "warning",
            "message": f"{high_risk_patients} paciente(s) com risco alto",
            "patient_id": None
        })
    
    return DashboardPsychologist(
        statistics=stats,
        upcoming_appointments=upcoming_appointments,
        recent_patients=recent_patients,
        alerts=alerts
    )

@router.get("/patient", response_model=DashboardPatient)
async def get_patient_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Estatísticas do paciente
    total_sessions = db.query(Appointment).filter(
        Appointment.patient_id == current_user.id
    ).count()
    
    completed_sessions = db.query(Appointment).filter(
        Appointment.patient_id == current_user.id,
        Appointment.status == AppointmentStatus.CONCLUIDO
    ).count()
    
    upcoming_sessions = db.query(Appointment).filter(
        Appointment.patient_id == current_user.id,
        Appointment.status == AppointmentStatus.AGENDADO,
        Appointment.date >= datetime.now().date()
    ).count()
    
    last_session = db.query(Appointment).filter(
        Appointment.patient_id == current_user.id,
        Appointment.status == AppointmentStatus.CONCLUIDO
    ).order_by(Appointment.date.desc()).first()
    
    statistics = {
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "upcoming_sessions": upcoming_sessions,
        "last_session_date": last_session.date if last_session else None
    }
    
    # Próximos agendamentos
    upcoming_appointments = db.query(Appointment).filter(
        Appointment.patient_id == current_user.id,
        Appointment.date >= datetime.now().date()
    ).order_by(Appointment.date, Appointment.time).limit(5).all()
    
    # Psicólogo
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    psychologist = None
    if patient:
        psychologist = db.query(User).filter(User.id == patient.psychologist_id).first()
    
    return DashboardPatient(
        statistics=statistics,
        upcoming_appointments=upcoming_appointments,
        psychologist=psychologist
    )