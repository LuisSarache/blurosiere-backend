import os
from typing import Optional

class SMSService:
    def __init__(self):
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.twilio_phone = os.getenv("TWILIO_PHONE_NUMBER", "")
        self.enabled = bool(self.twilio_sid and self.twilio_token)
    
    def send_sms(self, to: str, message: str) -> bool:
        if not self.enabled:
            print(f"📱 SMS simulado para {to}: {message}")
            return True
        
        try:
            # Importação condicional do Twilio
            from twilio.rest import Client
            
            client = Client(self.twilio_sid, self.twilio_token)
            
            message = client.messages.create(
                body=message,
                from_=self.twilio_phone,
                to=to
            )
            
            return True
        except ImportError:
            print("⚠️ Twilio não instalado. Use: pip install twilio")
            print(f"📱 SMS simulado para {to}: {message}")
            return False
        except Exception as e:
            print(f"❌ Erro ao enviar SMS: {e}")
            return False
    
    def send_appointment_reminder(self, to: str, date: str, time: str) -> bool:
        message = f"Lembrete: Você tem uma consulta agendada para {date} às {time}. BluRosiere"
        return self.send_sms(to, message)
    
    def send_urgent_alert(self, to: str, message: str) -> bool:
        alert = f"ALERTA: {message} - BluRosiere"
        return self.send_sms(to, alert)

sms_service = SMSService()