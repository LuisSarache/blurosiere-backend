from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.models import Schedule, User, UserType
from schemas.advanced_schemas import ScheduleCreate, ScheduleUpdate, Schedule as ScheduleSchema
from services.auth_service import get_current_user
import json

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.get("/", response_model=List[ScheduleSchema])
async def get_schedule(
    psychologist_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if psychologist_id:
        schedules = db.query(Schedule).filter(Schedule.psychologist_id == psychologist_id).all()
    else:
        if current_user.type != UserType.PSICOLOGO:
            raise HTTPException(status_code=403, detail="Apenas psicólogos podem acessar agenda")
        schedules = db.query(Schedule).filter(Schedule.psychologist_id == current_user.id).all()
    
    for schedule in schedules:
        schedule.exceptions = json.loads(schedule.exceptions) if schedule.exceptions else []
    
    return schedules

@router.post("/", response_model=ScheduleSchema)
async def create_schedule(
    schedule_data: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(status_code=403, detail="Apenas psicólogos podem criar agenda")
    
    schedule = Schedule(
        psychologist_id=current_user.id,
        day_of_week=schedule_data.day_of_week,
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time,
        slot_duration=schedule_data.slot_duration
    )
    
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    schedule.exceptions = []
    
    return schedule

@router.put("/{schedule_id}", response_model=ScheduleSchema)
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id,
        Schedule.psychologist_id == current_user.id
    ).first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Agenda não encontrada")
    
    for field, value in schedule_data.dict(exclude_unset=True).items():
        setattr(schedule, field, value)
    
    db.commit()
    db.refresh(schedule)
    schedule.exceptions = json.loads(schedule.exceptions) if schedule.exceptions else []
    
    return schedule

@router.delete("/{schedule_id}")
async def delete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id,
        Schedule.psychologist_id == current_user.id
    ).first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Agenda não encontrada")
    
    db.delete(schedule)
    db.commit()
    
    return {"message": "Horário removido com sucesso"}

@router.post("/exceptions")
async def add_exception(
    schedule_id: int,
    date: str,
    reason: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id,
        Schedule.psychologist_id == current_user.id
    ).first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Agenda não encontrada")
    
    exceptions = json.loads(schedule.exceptions) if schedule.exceptions else []
    exceptions.append(date)
    schedule.exceptions = json.dumps(exceptions)
    
    db.commit()
    
    return {"message": "Exceção adicionada com sucesso"}