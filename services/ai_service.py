import os
from typing import Optional

class AIService:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.huggingface_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.enabled = bool(self.openai_key or self.huggingface_key)
    
    def generate_response(self, message: str, context: Optional[str] = None) -> str:
        if not self.enabled:
            return self._fallback_response(message)
        
        if self.openai_key:
            return self._openai_response(message, context)
        elif self.huggingface_key:
            return self._huggingface_response(message, context)
        
        return self._fallback_response(message)
    
    def _openai_response(self, message: str, context: Optional[str]) -> str:
        try:
            import openai
            openai.api_key = self.openai_key
            
            messages = [
                {"role": "system", "content": "Você é um assistente virtual especializado em saúde mental e psicologia. Seja empático e profissional."}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"Contexto: {context}"})
            
            messages.append({"role": "user", "content": message})
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except ImportError:
            print("⚠️ openai não instalado. Use: pip install openai")
            return self._fallback_response(message)
        except Exception as e:
            print(f"❌ Erro OpenAI: {e}")
            return self._fallback_response(message)
    
    def _huggingface_response(self, message: str, context: Optional[str]) -> str:
        try:
            import requests
            
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            headers = {"Authorization": f"Bearer {self.huggingface_key}"}
            
            payload = {"inputs": message}
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                return response.json()[0]["generated_text"]
            else:
                return self._fallback_response(message)
        except Exception as e:
            print(f"❌ Erro HuggingFace: {e}")
            return self._fallback_response(message)
    
    def _fallback_response(self, message: str) -> str:
        # Respostas baseadas em regras simples
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["olá", "oi", "bom dia", "boa tarde", "boa noite"]):
            return "Olá! Como posso ajudá-lo hoje?"
        
        if any(word in message_lower for word in ["ajuda", "help", "socorro"]):
            return "Estou aqui para ajudar! Você pode me perguntar sobre agendamentos, consultas ou informações gerais sobre o sistema."
        
        if any(word in message_lower for word in ["agendar", "consulta", "horário"]):
            return "Para agendar uma consulta, acesse a seção de Agendamentos no menu principal. Lá você pode ver os horários disponíveis e marcar sua sessão."
        
        if any(word in message_lower for word in ["cancelar", "desmarcar"]):
            return "Para cancelar uma consulta, vá até 'Meus Agendamentos' e selecione a opção de cancelamento. Lembre-se que cancelamentos devem ser feitos com pelo menos 12 horas de antecedência."
        
        if any(word in message_lower for word in ["psicólogo", "terapeuta", "profissional"]):
            return "Você pode ver todos os psicólogos disponíveis na seção 'Profissionais'. Lá você encontra informações sobre especialidades e disponibilidade."
        
        return "Entendo sua mensagem. Como posso ajudá-lo especificamente? Posso auxiliar com agendamentos, informações sobre consultas ou dúvidas gerais sobre o sistema."

ai_service = AIService()