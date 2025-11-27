from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.models import Appointment, User, Patient, AppointmentStatus, UserType
from schemas.schemas import AppointmentCreate, AppointmentUpdate, AppointmentSchema
from services.auth_service import get_current_user
from services.email_service import send_email_appointment
 
router = APIRouter(prefix="/appointments", tags=["appointments"])
 
 
# ================================
# LISTAR AGENDAMENTOS
# ================================
@router.get("/", response_model=List[AppointmentSchema])
async def get_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type == UserType.PSICOLOGO:
        return db.query(Appointment).filter(
            Appointment.psychologist_id == current_user.id
        ).all()
 
    # Para pacientes → busca pelo e-mail do usuário
    patient = db.query(Patient).filter(Patient.email == current_user.email).first()
    if not patient:
        return []
 
    return db.query(Appointment).filter(
        Appointment.patient_id == patient.id
    ).all()
 
 
# ================================
# CRIAR AGENDAMENTO
# ================================
@router.post("/", response_model=AppointmentSchema)
async def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
 
    # Verifica horário disponível
    existing = db.query(Appointment).filter(
        Appointment.psychologist_id == appointment_data.psychologist_id,
        Appointment.date == appointment_data.date,
        Appointment.time == appointment_data.time,
        Appointment.status == AppointmentStatus.AGENDADO
    ).first()
 
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Horário não disponível"
        )
 
    # Criar agendamento
    db_appointment = Appointment(
        **appointment_data.dict(),
        status=AppointmentStatus.AGENDADO
    )
 
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
 
    # Buscar infos do paciente para enviar e-mail
    patient = db.query(Patient).filter(Patient.id == db_appointment.patient_id).first()
 
    if patient:
        send_email_appointment(
            client_email=patient.email,
            client_name=patient.name,
            date=db_appointment.date,
            time=db_appointment.time
        )
 
    return db_appointment
 
 
# ================================
# ATUALIZAR AGENDAMENTO
# ================================
@router.put("/{appointment_id}", response_model=AppointmentSchema)
async def update_appointment(
    appointment_id: int,
    update_data: AppointmentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
 
    if current_user.type == UserType.PSICOLOGO and appointment.psychologist_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para alterar este agendamento"
        )
 
    # Registrar o status atual antes da alteração
    old_status = appointment.status
 
    # Aplicar as mudanças
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(appointment, field, value)
 
    db.commit()
    db.refresh(appointment)
 
    # Verificar se o status foi alterado
    if old_status != appointment.status:
        # Buscar dados do paciente
        patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
        
        if patient:
            from services.email_service import send_email_appointment_status_update
            
            # Enviar notificação de mudança de status
            send_email_appointment_status_update(
                patient_email=patient.email,
                patient_name=patient.name,
                appointment_date=str(appointment.date),
                appointment_time=appointment.time,
                old_status=old_status.value,
                new_status=appointment.status.value
            )
 
    return appointment
 
 
# ================================
# CANCELAR AGENDAMENTO
# ================================
@router.delete("/{appointment_id}")
async def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
 
    # Buscar dados do paciente antes de cancelar
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    
    appointment.status = AppointmentStatus.CANCELADO
    db.commit()
    
    # Enviar e-mail de cancelamento
    if patient:
        from services.email_service import send_email_appointment_status_cancel
        send_email_appointment_status_cancel(
            patient_email=patient.email,
            patient_name=patient.name
        )
 
    return {"message": "Agendamento cancelado com sucesso"}
 
 
# ================================
# HORÁRIOS DISPONÍVEIS
# ================================
@router.get("/available-slots")
async def get_available_slots(
    date: str,
    psychologist_id: int,
    db: Session = Depends(get_db)
):
    all_slots = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
 
    occupied = db.query(Appointment.time).filter(
        Appointment.date == date,
        Appointment.psychologist_id == psychologist_id,
        Appointment.status == AppointmentStatus.AGENDADO
    ).all()
 
    occupied_times = [t[0] for t in occupied]
    available = [slot for slot in all_slots if slot not in occupied_times]
 
    return available
 
 