from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import User, Patient, UserType
from models.refresh_token import RefreshToken
from schemas.schemas import (
    UserCreate, UserLogin, Token, User as UserSchema,
    RefreshTokenRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from services.auth_service import authenticate_user
from utils import get_password_hash, create_access_token, calculate_age
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=timedelta(minutes=30)
    )
    
    # Criar refresh token
    refresh_token = RefreshToken.create_token(user.id)
    db.add(refresh_token)
    db.commit()
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token.token,
        user=UserSchema.from_orm(user)
    )

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verifica se usuário já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Cria novo usuário
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        type=user_data.type,
        specialty=user_data.specialty,
        crp=user_data.crp,
        phone=user_data.phone
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Se for paciente, cria registro na tabela de pacientes
    if user_data.type == UserType.PACIENTE and user_data.birth_date:
        age = calculate_age(user_data.birth_date)
        db_patient = Patient(
            id=db_user.id,
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone or "",
            birth_date=user_data.birth_date,
            age=age,
            status="Ativo"
        )
        db.add(db_patient)
        db.commit()
    
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=30)
    )
    
    # Criar refresh token
    refresh_token = RefreshToken.create_token(db_user.id)
    db.add(refresh_token)
    db.commit()
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token.token,
        user=UserSchema.from_orm(db_user)
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    # Buscar refresh token
    refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == token_data.refresh_token
    ).first()
    
    if not refresh_token or not refresh_token.is_valid():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    
    # Revogar token atual
    refresh_token.revoke()
    
    # Criar novos tokens
    user = refresh_token.user
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    
    new_refresh_token = RefreshToken.create_token(user.id)
    db.add(new_refresh_token)
    db.commit()
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=new_refresh_token.token,
        user=UserSchema.from_orm(user)
    )

@router.post("/logout")
async def logout(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    # Revogar refresh token
    refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == token_data.refresh_token
    ).first()
    
    if refresh_token:
        refresh_token.revoke()
        db.commit()
    
    return {"message": "Logout realizado com sucesso"}

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        # Por segurança, sempre retorna sucesso
        return {"message": "Se o email existir, você receberá instruções de recuperação"}
    
    # TODO: Implementar envio de email
    # Por enquanto, apenas log
    print(f"Password reset requested for: {user.email}")
    
    return {"message": "Se o email existir, você receberá instruções de recuperação"}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    # TODO: Implementar validação de token de reset
    # Por enquanto, apenas validação básica
    
    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senhas não coincidem"
        )
    
    # TODO: Buscar usuário pelo token e atualizar senha
    return {"message": "Senha alterada com sucesso"}