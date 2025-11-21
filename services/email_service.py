import os
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@blurosiere.com")
    
    def send_email(self, to: str, subject: str, body: str, html: bool = False):
        if not self.smtp_user or not self.smtp_password:
            print(f"📧 Email simulado para {to}: {subject}")
            return True
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
            return False
    
    def send_appointment_reminder(self, to: str, patient_name: str, date: str, time: str):
        subject = "Lembrete de Consulta - BluRosiere"
        body = f"""
        Olá {patient_name},
        
        Este é um lembrete da sua consulta agendada:
        
        Data: {date}
        Horário: {time}
        
        Por favor, confirme sua presença.
        
        Atenciosamente,
        Equipe BluRosiere
        """
        return self.send_email(to, subject, body)
    
    def send_appointment_confirmation(self, to: str, patient_name: str, date: str, time: str):
        subject = "Consulta Confirmada - BluRosiere"
        body = f"""
        Olá {patient_name},
        
        Sua consulta foi confirmada:
        
        Data: {date}
        Horário: {time}
        
        Atenciosamente,
        Equipe BluRosiere
        """
        return self.send_email(to, subject, body)
    
    def send_password_reset(self, to: str, reset_token: str):
        subject = "Recuperação de Senha - BluRosiere"
        reset_link = f"https://blurosiere.com/reset-password?token={reset_token}"
        body = f"""
        Você solicitou a recuperação de senha.
        
        Clique no link abaixo para redefinir sua senha:
        {reset_link}
        
        Este link expira em 1 hora.
        
        Se você não solicitou esta recuperação, ignore este email.
        
        Atenciosamente,
        Equipe BluRosiere
        """
        return self.send_email(to, subject, body)

email_service = EmailService()