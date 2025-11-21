from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime, timezone
import enum

class UserType(str, enum.Enum):
    PSICOLOGO = "psicologo"
    PACIENTE = "paciente"

class AppointmentStatus(str, enum.Enum):
    AGENDADO = "agendado"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"
    REAGENDADO = "reagendado"

class RequestStatus(str, enum.Enum):
    PENDENTE = "pendente"
    ACEITO = "aceito"
    REJEITADO = "rejeitado"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    type = Column(Enum(UserType))
    name = Column(String)
    specialty = Column(String, nullable=True)
    crp = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relacionamentos
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    avatar = Column(String, nullable=True)
    status = Column(String, default="ativo")
    bio = Column(Text, nullable=True)
    experience = Column(Integer, nullable=True)
    birth_date = Column(Date, nullable=True)
    emergency_contact = Column(String, nullable=True)
    medical_history = Column(Text, nullable=True)

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    birth_date = Column(Date)
    age = Column(Integer)
    status = Column(String)
    psychologist_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    psychologist = relationship("User", foreign_keys=[psychologist_id])

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    psychologist_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    time = Column(String)
    status = Column(Enum(AppointmentStatus))
    description = Column(String)
    duration = Column(Integer, default=50)
    notes = Column(Text, default="")
    full_report = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    patient = relationship("Patient")
    psychologist = relationship("User")

class Request(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    patient_email = Column(String)
    patient_phone = Column(String)
    preferred_psychologist = Column(Integer, ForeignKey("users.id"))
    description = Column(Text)
    urgency = Column(String)
    preferred_dates = Column(Text)  # JSON string
    preferred_times = Column(Text)  # JSON string
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDENTE)
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)
    
    psychologist = relationship("User")

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    psychologist_id = Column(Integer, ForeignKey("users.id"))
    day_of_week = Column(Integer)  # 0-6
    start_time = Column(String)
    end_time = Column(String)
    slot_duration = Column(Integer, default=50)
    is_active = Column(Boolean, default=True)
    exceptions = Column(Text, default="[]")  # JSON array of dates
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)
    
    psychologist = relationship("User")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # lembrete, confirmacao, cancelamento, alerta, sistema
    title = Column(String)
    message = Column(Text)
    read = Column(Boolean, default=False)
    action_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # user, assistant
    content = Column(Text)
    meta_data = Column(Text, default="{}")  # JSON
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    entity = Column(String)
    entity_id = Column(Integer)
    changes = Column(Text, default="{}")  # JSON
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    psychologist_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    type = Column(String)  # individual, geral, estatistico
    title = Column(String)
    content = Column(Text)
    data = Column(Text, default="{}")  # JSON
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    psychologist = relationship("User", foreign_keys=[psychologist_id])
    patient = relationship("User", foreign_keys=[patient_id])