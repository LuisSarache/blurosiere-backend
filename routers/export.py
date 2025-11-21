from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import User, Patient, Appointment, UserType
from services.auth_service import get_current_user
import csv
import io

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/patients")
async def export_patients(
    format: str = "csv",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(status_code=403, detail="Apenas psicólogos")
    
    patients = db.query(Patient).filter(Patient.psychologist_id == current_user.id).all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Nome', 'Email', 'Status', 'Risco', 'Total Sessões'])
        
        for patient in patients:
            user = db.query(User).filter(User.id == patient.user_id).first()
            writer.writerow([
                patient.id,
                user.name if user else '',
                user.email if user else '',
                patient.status,
                patient.risk_level,
                patient.total_sessions
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=patients.csv"}
        )
    
    raise HTTPException(status_code=400, detail="Formato não suportado")

@router.get("/appointments")
async def export_appointments(
    format: str = "csv",
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
    
    appointments = query.all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Data', 'Hora', 'Paciente', 'Status', 'Duração'])
        
        for apt in appointments:
            patient = db.query(User).filter(User.id == apt.patient_id).first()
            writer.writerow([
                apt.id,
                apt.date,
                apt.time,
                patient.name if patient else '',
                apt.status,
                apt.duration
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=appointments.csv"}
        )
    
    raise HTTPException(status_code=400, detail="Formato não suportado")