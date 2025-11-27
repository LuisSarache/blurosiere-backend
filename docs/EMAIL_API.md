# 📧 API de Email - Blurosiere

## Configuração

### 1. Instalar Dependências
```bash
pip install sib-api-v3-sdk
```

### 2. Configurar Variáveis de Ambiente
Adicione ao seu arquivo `.env`:
```env
BREVO_API_KEY=your-brevo-api-key-here
EMAIL_DOMAIN=no-reply@blurosiere.com
```

### 3. Obter API Key do Brevo
1. Acesse [Brevo (Sendinblue)](https://www.brevo.com/)
2. Crie uma conta gratuita
3. Vá em **Settings** → **SMTP & API** → **API Keys**
4. Crie uma nova API Key e copie

## Endpoints Disponíveis

### 📨 POST `/api/v1/email/send`
Envia um e-mail genérico personalizado.

**Body:**
```json
{
  "to_email": "destinatario@email.com",
  "subject": "Assunto do Email",
  "html_content": "<h1>Olá!</h1><p>Conteúdo HTML do email</p>",
  "sender_email": "remetente@email.com",
  "sender_name": "Nome do Remetente"
}
```

### 📅 POST `/api/v1/email/appointment`
Envia e-mail de confirmação de agendamento.

**Body:**
```json
{
  "client_email": "paciente@email.com",
  "client_name": "João Silva",
  "date": "2025-01-20",
  "time": "14:00"
}
```

### ✅ POST `/api/v1/email/request-accepted`
Envia e-mail notificando que a solicitação foi aceita.

**Body:**
```json
{
  "patient_email": "paciente@email.com",
  "patient_name": "Maria Santos",
  "psychologist_name": "Dra. Ana Costa"
}
```

## Exemplo de Uso

```bash
# Login
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"ana@test.com","password":"123456"}' \
  | jq -r '.access_token')

# Enviar email
curl -X POST "http://localhost:8000/api/v1/email/appointment" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "client_email": "paciente@email.com",
    "client_name": "João Silva",
    "date": "2025-01-20",
    "time": "14:00"
  }'
```
