# 🔌 Guia de Integrações - BluRosiere Backend

## 📋 Visão Geral

Este documento descreve todas as integrações externas disponíveis no sistema.

---

## 🌐 WebSocket (Tempo Real)

### Conexão
```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/${token}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Mensagem recebida:', data);
};
```

### Eventos Disponíveis

#### Notificações
```javascript
{
  "type": "notification:new",
  "data": {
    "id": 123,
    "title": "Nova Notificação",
    "message": "Você tem uma nova mensagem",
    "type": "lembrete"
  }
}
```

#### Agendamentos
```javascript
{
  "type": "appointment:updated",
  "data": {
    "id": 456,
    "status": "confirmado",
    "date": "2025-01-20"
  }
}
```

---

## 📧 Email (SMTP)

### Configuração

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@blurosiere.com
```

### Funcionalidades

- ✅ Lembretes de consulta
- ✅ Confirmações de agendamento
- ✅ Recuperação de senha
- ✅ Notificações de cancelamento

### Exemplo de Uso

```python
from services.email_service import email_service

email_service.send_appointment_reminder(
    to="patient@email.com",
    patient_name="João Silva",
    date="2025-01-20",
    time="14:00"
)
```

---

## 📱 SMS (Twilio)

### Configuração

```env
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE_NUMBER=+1234567890
```

### Instalação

```bash
pip install twilio
```

### Funcionalidades

- ✅ Lembretes urgentes
- ✅ Alertas de risco
- ✅ Confirmações rápidas

### Exemplo de Uso

```python
from services.sms_service import sms_service

sms_service.send_appointment_reminder(
    to="+5511999999999",
    date="2025-01-20",
    time="14:00"
)
```

---

## ☁️ Storage (AWS S3 / Local)

### Configuração Local

```env
STORAGE_TYPE=local
UPLOAD_DIR=uploads
```

### Configuração AWS S3

```env
STORAGE_TYPE=s3
AWS_S3_BUCKET=your-bucket
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

### Instalação

```bash
pip install boto3
```

### Endpoints

#### Upload de Avatar
```http
POST /api/v1/upload/avatar
Content-Type: multipart/form-data

file: [image file]
```

#### Upload de Anexo
```http
POST /api/v1/upload/attachment
Content-Type: multipart/form-data

file: [any file]
```

#### Upload Múltiplo
```http
POST /api/v1/upload/bulk
Content-Type: multipart/form-data

files: [multiple files]
```

### Limites

- Avatar: 5MB (JPEG, PNG, WebP)
- Anexos: 10MB por arquivo
- Bulk: Máximo 10 arquivos

---

## 🤖 IA (OpenAI / HuggingFace)

### Configuração OpenAI

```env
OPENAI_API_KEY=sk-your-key-here
```

### Configuração HuggingFace

```env
HUGGINGFACE_API_KEY=hf-your-key-here
```

### Instalação

```bash
# OpenAI
pip install openai

# HuggingFace (opcional)
pip install transformers
```

### Funcionalidades

- ✅ Chat assistente
- ✅ Respostas contextuais
- ✅ Fallback inteligente (sem API)

### Exemplo de Uso

```python
from services.ai_service import ai_service

response = ai_service.generate_response(
    message="Como agendar uma consulta?",
    context="Paciente novo"
)
```

---

## 🔔 Sistema de Notificações Integrado

### Canais Disponíveis

1. **In-App** (sempre ativo)
2. **Email** (se configurado)
3. **SMS** (se configurado)
4. **WebSocket** (tempo real)

### Exemplo Completo

```python
from services.notification_service import notification_service

# Envia por todos os canais configurados
notification_service.send_appointment_reminder(db, appointment)
```

---

## 🚀 Deploy e Produção

### Variáveis Obrigatórias

```env
SECRET_KEY=strong-random-key
DATABASE_URL=postgresql://user:pass@host/db
CORS_ORIGINS=https://yourdomain.com
```

### Variáveis Opcionais

Todas as integrações são opcionais. O sistema funciona sem elas, usando fallbacks:

- **Email**: Logs no console
- **SMS**: Logs no console
- **Storage**: Armazenamento local
- **IA**: Respostas baseadas em regras

### Recomendações de Produção

1. **Email**: Use SendGrid, AWS SES ou Mailgun
2. **SMS**: Use Twilio ou AWS SNS
3. **Storage**: Use AWS S3 ou Google Cloud Storage
4. **IA**: Use OpenAI GPT-3.5/4 ou HuggingFace

---

## 📊 Monitoramento

### Logs

Todos os serviços geram logs:

```python
print("📧 Email enviado para: user@email.com")
print("📱 SMS enviado para: +5511999999999")
print("☁️ Arquivo salvo: /uploads/avatars/file.jpg")
```

### Health Check

```http
GET /health
```

Retorna status de todas as integrações.

---

## 🔒 Segurança

### Boas Práticas

1. **Nunca commite** chaves de API
2. Use **variáveis de ambiente**
3. Rotacione **chaves regularmente**
4. Use **HTTPS** em produção
5. Valide **todos os uploads**

### Rate Limiting

- Email: 100/hora por usuário
- SMS: 10/hora por usuário
- Upload: 20/hora por usuário
- WebSocket: 1000 mensagens/hora

---

## 🆘 Troubleshooting

### Email não envia

```bash
# Teste SMTP
python -c "from services.email_service import email_service; email_service.send_email('test@email.com', 'Test', 'Body')"
```

### SMS não envia

```bash
# Verifique credenciais Twilio
echo $TWILIO_ACCOUNT_SID
```

### Upload falha

```bash
# Verifique permissões
mkdir -p uploads/avatars uploads/attachments
chmod 755 uploads
```

### WebSocket desconecta

- Verifique token JWT
- Confirme que o servidor suporta WebSocket
- Use proxy reverso adequado (nginx/caddy)

---

## 📞 Suporte

Para dúvidas sobre integrações:
- 📧 Email: integrations@blurosiere.com
- 📖 Docs: [Documentação Completa](./README.md)

---

**BluRosiere Integrations Guide v2.0.0**  
Sistema completo de integrações enterprise-grade