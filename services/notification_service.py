from sqlalchemy.orm import Session
from models.models import Notification, User, Appointment
from services.email_service import email_service
from services.sms_service import sms_service
from services.websocket_manager import manager
from datetime import datetime, timedelta
import asyncio

class NotificationService:
    
    @staticmethod
    def create_notification(db: Session, user_id: int, type: str, title: str, message: str, action_url: str = None):
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            action_url=action_url
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        # Enviar via WebSocket se conectado
        asyncio.create_task(manager.send_personal_message({
            "type": "notification:new",
            "data": {
                "id": notification.id,
                "title": title,
                "message": message,
                "type": type
            }
        }, user_id))
        
        return notification
    
    @staticmethod
    def send_appointment_reminder(db: Session, appointment: Appointment):
        user = db.query(User).filter(User.id == appointment.patient_id).first()
        if not user:
            return
        
        # Criar notificação
        NotificationService.create_notification(
            db,
            user.id,
            "lembrete",
            "Lembrete de Consulta",
            f"Você tem uma consulta agendada para {appointment.date} às {appointment.time}",
            f"/appointments/{appointment.id}"
        )
        
        # Enviar email
        email_service.send_appointment_reminder(
            user.email,
            user.name,
            str(appointment.date),
            appointment.time
        )
        
        # Enviar SMS se urgente
        if user.phone and appointment.type == "emergencia":
            sms_service.send_appointment_reminder(
                user.phone,
                str(appointment.date),
                appointment.time
            )
    
    @staticmethod
    def send_appointment_confirmation(db: Session, appointment: Appointment):
        user = db.query(User).filter(User.id == appointment.patient_id).first()
        if not user:
            return
        
        NotificationService.create_notification(
            db,
            user.id,
            "confirmacao",
            "Consulta Confirmada",
            f"Sua consulta foi confirmada para {appointment.date} às {appointment.time}",
            f"/appointments/{appointment.id}"
        )
        
        email_service.send_appointment_confirmation(
            user.email,
            user.name,
            str(appointment.date),
            appointment.time
        )
    
    @staticmethod
    def send_cancellation_notice(db: Session, appointment: Appointment, reason: str):
        user = db.query(User).filter(User.id == appointment.patient_id).first()
        if not user:
            return
        
        NotificationService.create_notification(
            db,
            user.id,
            "cancelamento",
            "Consulta Cancelada",
            f"Sua consulta de {appointment.date} às {appointment.time} foi cancelada. Motivo: {reason}",
            None
        )
    
    @staticmethod
    def send_risk_alert(db: Session, patient_id: int, risk_level: str, reason: str):
        # Notificar psicólogo
        from models.models import Patient
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return
        
        NotificationService.create_notification(
            db,
            patient.psychologist_id,
            "alerta",
            f"Alerta de Risco {risk_level.upper()}",
            f"Paciente com risco {risk_level}: {reason}",
            f"/patients/{patient_id}"
        )

notification_service = NotificationService()