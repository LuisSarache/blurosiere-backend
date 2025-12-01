from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/contact", tags=["contact"])

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str

@router.post("/")
async def send_contact_message(contact: ContactMessage):
    """Recebe mensagem do formulário de contato"""
    
    # Aqui você pode:
    # 1. Salvar no banco de dados
    # 2. Enviar email para o admin
    # 3. Criar notificação
    
    # Por enquanto, apenas retorna sucesso
    return {
        "success": True,
        "message": "Mensagem enviada com sucesso! Entraremos em contato em breve.",
        "data": {
            "name": contact.name,
            "email": contact.email,
            "received_at": datetime.now().isoformat()
        }
    }
