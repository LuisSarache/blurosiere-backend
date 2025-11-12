# Blurosiere Backend

Sistema completo de agendamento psicológico desenvolvido com FastAPI, incluindo análise de risco com Machine Learning.

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8+
- pip

### Configuração
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd blurosiere-backend

# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados
python seed_data.py

# Execute o servidor
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

## 📚 Documentação da API

Acesse `http://localhost:8000/docs` para ver a documentação interativa completa.

## 🔐 Autenticação

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "ana@test.com",
  "password": "123456"
}
```

### Usuários de Teste
- **Psicólogos**: 
  - `ana@test.com` / `123456` (Dra. Ana Costa - TCC)
  - `carlos@test.com` / `123456` (Dr. Carlos Mendes - Infantil)
  - `lucia@test.com` / `123456` (Dra. Lucia Ferreira - Familiar)
- **Paciente**: `paciente@test.com` / `123456`

## 📋 Endpoints Principais

### 🔐 Autenticação (/auth)
- `POST /auth/login` - Login de usuário
- `POST /auth/register` - Registro de novo usuário

### 👥 Pacientes (/patients)
- `GET /patients/` - Listar pacientes do psicólogo
- `GET /patients/{id}` - Detalhes de um paciente
- `POST /patients/` - Cadastrar novo paciente
- `GET /patients/{id}/sessions` - Sessões do paciente

### 🧠 Psicólogos (/psychologists)
- `GET /psychologists/` - Listar todos os psicólogos

### 📅 Agendamentos (/appointments)
- `GET /appointments/` - Listar agendamentos do psicólogo
- `GET /appointments/{id}` - Detalhes de um agendamento
- `POST /appointments/` - Criar novo agendamento
- `PUT /appointments/{id}` - Atualizar agendamento
- `DELETE /appointments/{id}` - Cancelar agendamento
- `GET /appointments/available-times` - Horários disponíveis

### 📋 Solicitações (/requests)
- `GET /requests/` - Listar solicitações (apenas psicólogos)
- `POST /requests/` - Criar nova solicitação
- `PUT /requests/{id}` - Atualizar status da solicitação

### 📊 Relatórios (/reports)
- `GET /reports/{psychologist_id}` - Relatório completo do psicólogo

### 🤖 Análise ML (/ml)
- `GET /ml/risk-analysis` - Análise de risco geral
- `GET /ml/risk-analysis/{patient_id}` - Análise individual

## 📝 Exemplos de Uso

### Criar Solicitação
```json
{
  "patient_name": "João Silva",
  "patient_email": "joao@email.com",
  "patient_phone": "11999999999",
  "preferred_psychologist": 2,
  "description": "Preciso de ajuda com ansiedade",
  "preferred_dates": ["2025-01-15", "2025-01-16"],
  "preferred_times": ["09:00", "14:00"],
  "urgency": "media"
}
```

### Criar Agendamento
```json
{
  "patient_id": 5,
  "date": "2025-01-20",
  "time": "14:00",
  "description": "Sessão de terapia cognitivo-comportamental",
  "duration": 50
}
```

### Valores Aceitos
- **Urgency**: `baixa`, `media`, `alta`
- **Status Solicitação**: `pendente`, `aceito`, `rejeitado`
- **Status Agendamento**: `agendado`, `concluido`, `cancelado`, `reagendado`
- **Tipo Usuário**: `psicologo`, `paciente`

## 🧪 Testes

Execute os testes automatizados completos:
```bash
python test_fixed.py
```

Teste específico de autenticação:
```bash
python test_debug.py
```

## 🤖 Funcionalidades de ML

O sistema inclui análise de risco baseada em Machine Learning que avalia:
- Frequência de consultas
- Taxa de cancelamentos
- Tempo desde última consulta
- Tendências de comparecimento
- Padrões comportamentais

### Níveis de Risco
- **Alto**: Score ≥ 70 (requer atenção imediata)
- **Moderado**: Score 40-69 (monitoramento necessário)
- **Baixo**: Score < 40 (padrão normal)

## 📁 Estrutura do Projeto

```
blurosiere-backend/
├── core/
│   └── database.py          # Configuração do banco SQLite
├── models/
│   └── models.py           # Modelos SQLAlchemy
├── routers/
│   ├── auth.py            # Autenticação e registro
│   ├── requests.py        # Solicitações de atendimento
│   ├── patients.py        # Gestão de pacientes
│   ├── psychologists.py   # Listagem de psicólogos
│   ├── appointments.py    # Agendamentos e sessões
│   ├── reports.py         # Relatórios e estatísticas
│   └── ml_analysis.py     # Análise de risco ML
├── schemas/
│   └── schemas.py         # Schemas Pydantic
├── services/
│   ├── auth_service.py    # Serviços de autenticação
│   ├── report_service.py  # Geração de relatórios
│   └── ml_service.py      # Algoritmos de ML
├── main.py               # Aplicação principal FastAPI
├── seed_data.py         # Dados de teste e seed
├── utils.py             # Funções utilitárias
└── requirements.txt     # Dependências Python
```

## 🔧 Troubleshooting

### Erro 500 em endpoints
1. Execute `python seed_data.py` para recriar o banco
2. Verifique se está logado como psicólogo
3. Confirme que o servidor está rodando
4. Verifique logs do servidor para detalhes

### Erro 403 Forbidden
- Apenas psicólogos podem acessar dados de pacientes
- Use `ana@test.com` para testes como psicólogo

### Erro 401 Unauthorized
- Token expirado ou inválido
- Faça login novamente para obter novo token

### Erro 422 Validation Error
- Dados de entrada inválidos
- Verifique formato de email, datas e campos obrigatórios

### Erro 404 Not Found
- Verifique se o endpoint existe
- Confirme IDs de recursos (paciente, agendamento, etc.)
- Alguns endpoints requerem barra final: `/requests/`

## 🎯 Funcionalidades Implementadas

✅ Sistema completo de autenticação JWT  
✅ Gestão de pacientes e psicólogos  
✅ Agendamento de consultas  
✅ Solicitações de atendimento  
✅ Relatórios estatísticos  
✅ Análise de risco com ML  
✅ Validação de dados com Pydantic  
✅ Documentação automática OpenAPI  
✅ Testes automatizados  
✅ Banco de dados SQLite  
✅ CORS configurado  
✅ Tratamento de erros  

## 📈 Próximas Funcionalidades

🔄 Sistema de notificações  
🔄 Integração com calendário  
🔄 Backup automático  
🔄 Dashboard web  
🔄 API de pagamentos  