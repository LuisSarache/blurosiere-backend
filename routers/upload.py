from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.models import User, UserType
from services.auth_service import get_current_user
from services.storage_service import storage_service

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validar tipo de arquivo
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido")
    
    # Validar tamanho (5MB)
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo muito grande (máx 5MB)")
    
    # Salvar arquivo
    file_url = storage_service.save_file(content, file.filename, "avatars")
    
    # Deletar avatar antigo se existir
    if current_user.avatar:
        storage_service.delete_file(current_user.avatar)
    
    # Atualizar usuário
    current_user.avatar = file_url
    db.commit()
    
    return {"avatar_url": file_url}

@router.post("/attachment")
async def upload_attachment(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(status_code=403, detail="Apenas psicólogos podem fazer upload de anexos")
    
    # Validar tamanho (10MB)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo muito grande (máx 10MB)")
    
    # Salvar arquivo
    file_url = storage_service.save_file(content, file.filename, "attachments")
    
    return {"file_url": file_url, "filename": file.filename}

@router.post("/bulk")
async def upload_multiple(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(status_code=403, detail="Apenas psicólogos")
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Máximo 10 arquivos por vez")
    
    uploaded_files = []
    
    for file in files:
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            continue
        
        file_url = storage_service.save_file(content, file.filename, "attachments")
        uploaded_files.append({"filename": file.filename, "url": file_url})
    
    return {"files": uploaded_files, "count": len(uploaded_files)}

@router.delete("/file")
async def delete_file(
    file_url: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if storage_service.delete_file(file_url):
        return {"message": "Arquivo deletado com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")