from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from core.database import get_db
from models.models import User, Patient, Appointment, AppointmentStatus, UserType
from schemas.advanced_schemas import AnalyticsOverview, AnalyticsTrends
from services.auth_service import get_current_user
from datetime import datetime, timedelta
from typing import List

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    start_date: str = None,
    end_date: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(status_code=403, detail="Apenas psicólogos")
    
    query = db.query(Appointment).filter(Appointment.psychologist_id == current_user.id)
    
    if start_date:
        query = query.filter(Appointment.date >= start_date)
    if end_date:
        query = query.filter(Appointment.date <= end_date)
    
    total_sessions = query.count()
    total_patients = db.query(Patient).filter(Patient.psychologist_id == current_user.id).count()
    
    avg_sessions = total_sessions / total_patients if total_patients > 0 else 0
    
    # Sessões por status
    sessions_by_status = db.query(
        Appointment.status,
        func.count(Appointment.id).label('count')
    ).filter(
        Appointment.psychologist_id == current_user.id
    ).group_by(Appointment.status).all()
    
    sessions_status_data = [
        {
            "status": str(status),
            "count": count,
            "percentage": round(count / total_sessions * 100, 2) if total_sessions > 0 else 0
        }
        for status, count in sessions_by_status
    ]
    
    # Sessões por mês
    sessions_by_month = db.query(
        extract('month', Appointment.date).label('month'),
        func.count(Appointment.id).label('count')
    ).filter(
        Appointment.psychologist_id == current_user.id
    ).group_by('month').all()
    
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    sessions_month_data = [
        {"month": months[int(month)-1], "count": count}
        for month, count in sessions_by_month
    ]
    
    # Pacientes por nível de risco
    patients_by_risk = db.query(
        Patient.risk_level,
        func.count(Patient.id).label('count')
    ).filter(
        Patient.psychologist_id == current_user.id
    ).group_by(Patient.risk_level).all()
    
    risk_data = [
        {"level": level or "baixo", "count": count}
        for level, count in patients_by_risk
    ]
    
    return AnalyticsOverview(
        total_sessions=total_sessions,
        total_patients=total_patients,
        average_sessions_per_patient=round(avg_sessions, 2),
        sessions_by_status=sessions_status_data,
        sessions_by_month=sessions_month_data,
        patients_by_risk_level=risk_data,
        top_cancellation_reasons=[]
    )

@router.get("/trends", response_model=AnalyticsTrends)
async def get_analytics_trends(
    metric: str = "sessions",
    period: str = "month",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(status_code=403, detail="Apenas psicólogos")
    
    # Dados simulados por enquanto
    data = [
        {"date": "2025-01", "value": 45},
        {"date": "2025-02", "value": 52},
        {"date": "2025-03", "value": 48}
    ]
    
    return AnalyticsTrends(
        data=data,
        trend="up",
        change_percentage=8.5
    )