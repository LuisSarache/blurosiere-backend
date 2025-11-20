"""
Constantes da aplicação Blurosiere
"""

# Status de usuários
USER_TYPES = {
    "PSYCHOLOGIST": "psicologo",
    "PATIENT": "paciente"
}

# Status de agendamentos
APPOINTMENT_STATUS = {
    "SCHEDULED": "agendado",
    "COMPLETED": "concluido", 
    "CANCELLED": "cancelado",
    "RESCHEDULED": "reagendado"
}

# Status de solicitações
REQUEST_STATUS = {
    "PENDING": "pendente",
    "ACCEPTED": "aceito",
    "REJECTED": "rejeitado"
}

# Níveis de urgência
URGENCY_LEVELS = {
    "LOW": "baixa",
    "MEDIUM": "media", 
    "HIGH": "alta"
}

# Níveis de risco ML
RISK_LEVELS = {
    "LOW": "baixo",
    "MODERATE": "moderado",
    "HIGH": "alto"
}

# Durações padrão de sessões (em minutos)
SESSION_DURATIONS = {
    "SHORT": 30,
    "STANDARD": 50,
    "EXTENDED": 60,
    "DOUBLE": 90
}

# Horários de funcionamento
BUSINESS_HOURS = {
    "START": "08:00",
    "END": "18:00",
    "LUNCH_START": "12:00", 
    "LUNCH_END": "13:00"
}

# Limites de paginação
PAGINATION = {
    "DEFAULT_LIMIT": 20,
    "MAX_LIMIT": 100
}

# Mensagens de erro padrão
ERROR_MESSAGES = {
    "UNAUTHORIZED": "Credenciais inválidas",
    "FORBIDDEN": "Acesso negado",
    "NOT_FOUND": "Recurso não encontrado",
    "VALIDATION_ERROR": "Dados inválidos",
    "INTERNAL_ERROR": "Erro interno do servidor",
    "DATABASE_ERROR": "Erro de conexão com banco de dados"
}

# Mensagens de sucesso
SUCCESS_MESSAGES = {
    "CREATED": "Criado com sucesso",
    "UPDATED": "Atualizado com sucesso", 
    "DELETED": "Removido com sucesso",
    "LOGIN_SUCCESS": "Login realizado com sucesso"
}