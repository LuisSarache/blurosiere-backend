from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from core.database import get_db
from models.models import User, Patient, Appointment, UserType
from schemas.advanced_schemas import SearchResults
from services.auth_service import get_current_user

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/", response_model=SearchResults)
async def search(
    q: str,
    type: str = "all",
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(status_code=403, detail="Apenas psicólogos")
    
    results = {"patients": [], "appointments": [], "total": 0}
    
    if type in ["patients", "all"]:
        patients = db.query(Patient).join(User).filter(
            Patient.psychologist_id == current_user.id,
            or_(
                User.name.ilike(f"%{q}%"),
                User.email.ilike(f"%{q}%")
            )
        ).limit(limit).all()
        results["patients"] = patients
        results["total"] += len(patients)
    
    if type in ["appointments", "all"]:
        appointments = db.query(Appointment).filter(
            Appointment.psychologist_id == current_user.id,
            or_(
                Appointment.description.ilike(f"%{q}%"),
                Appointment.notes.ilike(f"%{q}%")
            )
        ).limit(limit).all()
        results["appointments"] = appointments
        results["total"] += len(appointments)
    
    return results