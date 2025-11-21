from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from services.websocket_manager import manager
from jose import jwt, JWTError
from utils import SECRET_KEY, ALGORITHM
from models.models import User
import json

router = APIRouter()

async def get_user_from_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email:
            return db.query(User).filter(User.email == email).first()
    except JWTError:
        return None
    return None

@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    user = await get_user_from_token(token, db)
    
    if not user:
        await websocket.close(code=1008)
        return
    
    await manager.connect(websocket, user.id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Echo back para teste
            await manager.send_personal_message({
                "type": "echo",
                "data": message
            }, user.id)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)