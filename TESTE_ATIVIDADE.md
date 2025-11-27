# 🧪 GUIA DE TESTES - ATIVIDADE NOTIFICAÇÃO DE STATUS

## 📋 **Pré-requisitos**

1. **Servidor rodando:**
```bash
uvicorn main:app --reload
```

2. **Acesse o Swagger:** http://localhost:8000/docs

3. **Dados inseridos no banco:**
```bash
python seed_data.py
```

---

## 🔐 **PASSO 1: LOGIN**

### **Endpoint:** `POST /api/v1/auth/login`

### **JSON:**
```json
{
  "email": "psicologo.2025@outlook.com",
  "password": "123456"
}
```

### **Resultado esperado:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### **Ação:**
1. **Copie o `access_token`**
2. **Clique em "Authorize"** no topo do Swagger
3. **Cole o token** (sem "Bearer ")
4. **Clique em "Authorize" e "Close"**

---

## 📅 **PASSO 2: CRIAR AGENDAMENTO**

### **Endpoint:** `POST /api/v1/appointments/`

### **JSON:**
```json
{
  "patient_id": 1,
  "psychologist_id": 1,
  "date": "2025-11-26",
  "time": "14:00",
  "description": "teste",
  "duration": 50
}
```

### **Resultado esperado:**
```json
{
  "id": 1,
  "patient_id": 1,
  "psychologist_id": 1,
  "date": "2025-11-26",
  "time": "14:00",
  "status": "agendado",
  "description": "teste",
  "duration": 50,
  "created_at": "2025-11-26T..."
}
```

### **✅ Verificações:**
- [ ] Status HTTP: **201 Created**
- [ ] **Anote o `id` retornado** (ex: 1)
- [ ] Status inicial: **"agendado"**
- [ ] **Email enviado** para `paciente.2025@outlook.com`

---

## 🔄 **PASSO 3: ATUALIZAR STATUS (PUT)**

### **Endpoint:** `PUT /api/v1/appointments/{id}`
*Substitua `{id}` pelo ID do agendamento criado*

### **JSON (apenas status):**
```json
{
  "status": "reagendado"
}
```

### **OU JSON (status + horário):**
```json
{
  "time": "15:00",
  "status": "reagendado"
}
```

### **Resultado esperado:**
```json
{
  "id": 1,
  "patient_id": 1,
  "psychologist_id": 1,
  "date": "2025-11-26",
  "time": "15:00",
  "status": "reagendado",
  "description": "teste reagendado",
  "duration": 50
}
```

### **✅ Verificações:**
- [ ] Status HTTP: **200 OK**
- [ ] Status mudou: **"agendado" → "reagendado"**
- [ ] **Email automático enviado** com mudança de status
- [ ] Email mostra: status anterior vs novo status

---

## ❌ **PASSO 4: CANCELAR AGENDAMENTO (DELETE)**

### **Endpoint:** `DELETE /api/v1/appointments/{id}`
*Substitua `{id}` pelo ID do agendamento*

### **Sem JSON** (DELETE não precisa de body)

### **Resultado esperado:**
```json
{
  "message": "Agendamento cancelado com sucesso"
}
```

### **✅ Verificações:**
- [ ] Status HTTP: **200 OK**
- [ ] **Email de cancelamento enviado**
- [ ] Status no banco: **"cancelado"**

---

## 📧 **EMAILS ENVIADOS**

### **1. POST - Confirmação:**
- **Para:** `paciente.2025@outlook.com`
- **Assunto:** "Confirmação de Agendamento"
- **Conteúdo:** Data e horário da consulta

### **2. PUT - Mudança de Status:**
- **Para:** `paciente.2025@outlook.com`
- **Assunto:** "Atualização de Status do Agendamento"
- **Conteúdo:** Status anterior vs novo status

### **3. DELETE - Cancelamento:**
- **Para:** `paciente.2025@outlook.com`
- **Assunto:** "Agendamento Cancelado"
- **Conteúdo:** Informação sobre cancelamento

---

## 🚨 **POSSÍVEIS ERROS**

### **401 Unauthorized**
- **Causa:** Token expirado ou inválido
- **Solução:** Faça login novamente

### **422 Unprocessable Entity**
- **Causa:** JSON inválido (vírgulas extras, campos obrigatórios)
- **Causa:** Campo `date` deve ser None no PUT
- **Solução:** Envie apenas os campos que quer alterar
- **Solução:** Para mudar status: `{"status": "reagendado"}`

### **404 Not Found**
- **Causa:** ID do agendamento não existe
- **Solução:** Use o ID correto retornado no POST

### **403 Forbidden**
- **Causa:** Usuário sem permissão
- **Solução:** Login como psicólogo

---

## 📝 **CHECKLIST FINAL**

- [ ] **Login realizado** com sucesso
- [ ] **Token autorizado** no Swagger
- [ ] **Agendamento criado** (POST)
- [ ] **Email de confirmação** enviado
- [ ] **Status atualizado** (PUT)
- [ ] **Email de mudança** enviado
- [ ] **Agendamento cancelado** (DELETE)
- [ ] **Email de cancelamento** enviado

---

## 🎯 **OBJETIVO DA ATIVIDADE**

✅ **Implementar notificação automática por email quando:**
1. Status do agendamento for alterado (PUT)
2. Agendamento for cancelado (DELETE)

✅ **Funções implementadas:**
- `send_email_appointment_status_update()`
- `send_email_appointment_status_cancel()`

✅ **Integração nas rotas:**
- PUT: Verifica mudança de status e envia email
- DELETE: Envia email de cancelamento

---

**🎉 SUCESSO!** Se todos os passos funcionaram, a atividade está completa!