# Blurosiere Backend

Sistema de agendamento psicológico desenvolvido com FastAPI.

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

Acesse `http://localhost:8000/docs` para ver a documentação interativa.

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
- **Psicólogo**: `ana@test.com` / `123456`
- **Paciente**: `paciente@test.com` / `123456`

## 📋 Endpoints Principais

### Solicitações (/requests)
- `GET /requests/` - Listar solicitações (apenas psicólogos)
- `POST /requests/` - Criar nova solicitação
- `PUT /requests/{id}` - Atualizar status da solicitação

### Exemplo de Criação de Solicitação
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

### Valores Aceitos
- **Urgency**: `baixa`, `media`, `alta`
- **Status**: `pendente`, `aceito`, `rejeitado`

## 🧪 Testes

Execute os testes automatizados:
```bash
python test_fixed.py
```

## 📁 Estrutura do Projeto

```
blurosiere-backend/
├── core/
│   └── database.py          # Configuração do banco
├── models/
│   └── models.py           # Modelos SQLAlchemy
├── routers/
│   ├── auth.py            # Autenticação
│   ├── requests.py        # Solicitações
│   ├── patients.py        # Pacientes
│   ├── psychologists.py   # Psicólogos
│   └── appointments.py    # Agendamentos
├── schemas/
│   └── schemas.py         # Schemas Pydantic
├── services/
│   └── auth_service.py    # Serviços de autenticação
├── main.py               # Aplicação principal
├── seed_data.py         # Dados de teste
└── requirements.txt     # Dependências
```

## 🔧 Troubleshooting

### Erro 500 em /requests
1. Execute `python seed_data.py` para recriar o banco
2. Verifique se está logado como psicólogo
3. Confirme que o servidor está rodando

### Erro 403 Forbidden
- Apenas psicólogos podem listar solicitações
- Use `ana@test.com` para testes

### Erro 404 Not Found
- Verifique se o endpoint tem a barra final correta
- GET/POST: `/requests/` (com barra)
- PUT: `/requests/{id}` (sem barra)