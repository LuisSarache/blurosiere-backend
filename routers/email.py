from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from services.email_service import send_email, send_email_appointment, send_email_request_accepted
from services.auth_service import get_current_user
from models.models import User

router = APIRouter(prefix="/email", tags=["Email"])

# =============================
# SCHEMAS
# =============================
class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    html_content: str
    sender_email: Optional[str] = None
    sender_name: Optional[str] = None

class AppointmentEmailRequest(BaseModel):
    client_email: EmailStr
    client_name: str
    date: str
    time: str

class RequestAcceptedEmailRequest(BaseModel):
    patient_email: EmailStr
    patient_name: str
    psychologist_name: str

# =============================
# ENDPOINTS
# =============================
@router.post("/send")
async def send_generic_email(
    email_data: EmailRequest,
    current_user: User = Depends(get_current_user)
):
    """Envia um e-mail genérico"""
    try:
        success = send_email(
            to_email=email_data.to_email,
            subject=email_data.subject,
            html_content=email_data.html_content,
            sender_email=email_data.sender_email,
            sender_name=email_data.sender_name
        )
        if success:
            return {"message": "E-mail enviado com sucesso", "to": email_data.to_email}
        raise HTTPException(status_code=500, detail="Falha ao enviar e-mail")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar e-mail: {str(e)}")

@router.post("/appointment")
async def send_appointment_confirmation(
    email_data: AppointmentEmailRequest,
    current_user: User = Depends(get_current_user)
):
    """Envia e-mail de confirmação de agendamento"""
    try:
        success = send_email_appointment(
            client_email=email_data.client_email,
            client_name=email_data.client_name,
            date=email_data.date,
            time=email_data.time
        )
        if success:
            return {"message": "E-mail de confirmação enviado", "to": email_data.client_email}
        raise HTTPException(status_code=500, detail="Falha ao enviar e-mail")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar e-mail: {str(e)}")

@router.post("/request-accepted")
async def send_request_accepted_notification(
    email_data: RequestAcceptedEmailRequest,
    current_user: User = Depends(get_current_user)
):
    """Envia e-mail notificando que a solicitação foi aceita"""
    try:
        success = send_email_request_accepted(
            patient_email=email_data.patient_email,
            patient_name=email_data.patient_name,
            psychologist_name=email_data.psychologist_name
        )
        if success:
            return {"message": "E-mail de notificação enviado", "to": email_data.patient_email}
        raise HTTPException(status_code=500, detail="Falha ao enviar e-mail")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar e-mail: {str(e)}")
