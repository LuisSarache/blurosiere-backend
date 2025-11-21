from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.models import ChatMessage, User
from schemas.advanced_schemas import ChatMessageCreate, ChatMessage as ChatMessageSchema
from services.auth_service import get_current_user
import json

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
async def send_message(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Salvar mensagem do usuário
    user_message = ChatMessage(
        user_id=current_user.id,
        role="user",
        content=message_data.message,
        metadata=json.dumps({"context": message_data.context})
    )
    db.add(user_message)
    db.commit()
    
    # Gerar resposta da IA (simulada por enquanto)
    ai_response = f"Entendo sua mensagem: '{message_data.message}'. Como posso ajudar mais?"
    
    # Salvar resposta da IA
    ai_message = ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=ai_response,
        metadata=json.dumps({})
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)
    
    return {
        "response": ai_response,
        "message_id": ai_message.id
    }

@router.get("/history", response_model=List[ChatMessageSchema])
async def get_history(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.created_at.desc()).offset(offset).limit(limit).all()
    
    for msg in messages:
        msg.metadata = json.loads(msg.metadata) if msg.metadata else {}
    
    return messages

@router.delete("/history")
async def clear_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(ChatMessage).filter(ChatMessage.user_id == current_user.id).delete()
    db.commit()
    
    return {"message": "Histórico limpo com sucesso"}