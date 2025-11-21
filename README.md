# Blurosiere Backend

<div align="center">
  <h3>🌹 Sistema Completo de Agendamento Psicológico 🌹</h3>
  <p>API moderna desenvolvida com FastAPI, incluindo análise de risco com Machine Learning</p>
  
  ![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
  ![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
  ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
  ![License](https://img.shields.io/badge/License-MIT-yellow.svg)
</div>

## 🎆 Funcionalidades

### Core
- 🔐 **Autenticação JWT** - Login, refresh tokens, recuperação de senha
- 👥 **Gestão de Pacientes** - CRUD completo com histórico e nível de risco
- 🧠 **Gestão de Psicólogos** - Perfis, especialidades e agendas
- 📅 **Agendamentos** - Sistema completo de consultas e horários
- 📋 **Solicitações** - Workflow de aprovação e gestão

### Avançado
- 📆 **Sistema de Agenda** - Horários, slots e exceções
- 🔔 **Notificações** - Sistema completo de alertas e lembretes
- 🤖 **Chat IA** - Assistente virtual inteligente
- 📊 **Dashboard** - Estatísticas em tempo real
- 📈 **Analytics** - Métricas avançadas e tendências
- 🔍 **Busca** - Sistema de busca avançado
- 📤 **Exportação** - Dados em CSV/Excel
- 📊 **Relatórios** - Geração automática
- 🤖 **Análise ML** - Detecção de risco com IA
- 📚 **Documentação** - OpenAPI/Swagger automática

## 🚀 Instalação Rápida

### Método 1: Instalação Local

```bash
# Clone o repositório
git clone https://github.com/LuisSarache/blurosiere-backend.git
cd blurosiere-backend

# Crie ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Initialize banco de dados
python seed_data.py

# Execute o servidor
python main.py
# ou
uvicorn main:app --reload
```

### Método 2: Docker (Recomendado para Produção)

```bash
# Clone e entre no diretório
git clone https://github.com/LuisSarache/blurosiere-backend.git
cd blurosiere-backend

# Execute com Docker Compose
docker-compose up -d

# Para ambiente de produção
docker-compose --profile production up -d
```

## 🌍 Acesso

- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Info**: http://localhost:8000/api/v1/info

## 🔑 Autenticação

### Usuários de Teste

| Tipo | Email | Senha | Descrição |
|------|-------|-------|-------------|
| Psicólogo | `ana@test.com` | `123456` | Dra. Ana Costa - TCC |
| Psicólogo | `carlos@test.com` | `123456` | Dr. Carlos Mendes - Infantil |
| Psicólogo | `lucia@test.com` | `123456` | Dra. Lucia Ferreira - Familiar |
| Paciente | `paciente@test.com` | `123456` | Maria Santos |

### Exemplo de Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "ana@test.com",
       "password": "123456"
     }'
```

## 📚 API Endpoints

### 🔐 Autenticação (`/api/v1/auth`)
- `POST /login` - Login de usuário
- `POST /register` - Registro de novo usuário

### 👥 Pacientes (`/api/v1/patients`)
- `GET /` - Listar pacientes do psicólogo
- `GET /{id}` - Detalhes de um paciente
- `POST /` - Cadastrar novo paciente
- `GET /{id}/sessions` - Sessões do paciente

### 🧠 Psicólogos (`/api/v1/psychologists`)
- `GET /` - Listar todos os psicólogos

### 📅 Agendamentos (`/api/v1/appointments`)
- `GET /` - Listar agendamentos do psicólogo
- `GET /{id}` - Detalhes de um agendamento
- `POST /` - Criar novo agendamento
- `PUT /{id}` - Atualizar agendamento
- `DELETE /{id}` - Cancelar agendamento
- `GET /available-times` - Horários disponíveis

### 📋 Solicitações (`/api/v1/requests`)
- `GET /` - Listar solicitações (apenas psicólogos)
- `POST /` - Criar nova solicitação
- `PUT /{id}` - Atualizar status da solicitação

### 📊 Relatórios (`/api/v1/reports`)
- `GET /{psychologist_id}` - Relatório completo do psicólogo

### 🤖 Análise ML (`/api/v1/ml`)
- `GET /risk-analysis` - Análise de risco geral
- `GET /risk-analysis/{patient_id}` - Análise individual

### 📆 Agenda (`/api/v1/schedule`)
- `GET /` - Listar horários da agenda
- `POST /` - Criar novo horário
- `PUT /{id}` - Atualizar horário
- `DELETE /{id}` - Remover horário
- `POST /exceptions` - Adicionar exceção

### 🔔 Notificações (`/api/v1/notifications`)
- `GET /` - Listar notificações
- `GET /unread-count` - Contador de não lidas
- `PUT /{id}/read` - Marcar como lida
- `PUT /read-all` - Marcar todas como lidas
- `DELETE /{id}` - Remover notificação

### 🤖 Chat IA (`/api/v1/chat`)
- `POST /message` - Enviar mensagem
- `GET /history` - Histórico de conversa
- `DELETE /history` - Limpar histórico

### 📊 Dashboard (`/api/v1/dashboard`)
- `GET /psychologist` - Dashboard do psicólogo
- `GET /patient` - Dashboard do paciente

### 📈 Analytics (`/api/v1/analytics`)
- `GET /overview` - Visão geral de estatísticas
- `GET /trends` - Tendências e métricas

### 🔍 Busca (`/api/v1/search`)
- `GET /` - Busca avançada

### 📤 Exportação (`/api/v1/export`)
- `GET /patients` - Exportar pacientes
- `GET /appointments` - Exportar agendamentos

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

## 🧪 Testes Automatizados

```bash
# Execute todos os testes
python test_fixed.py

# Testes com pytest (se instalado)
pytest tests/ -v

# Testes de cobertura
pytest --cov=. tests/
```

### Resultado Esperado
```
🧪 INICIANDO TESTES AUTOMATIZADOS - BLUROSIERE API
============================================================
🏥 TESTANDO SAÚDE DO SERVIDOR
✅ Servidor rodando
✅ Health check
✅ API info

🔐 TESTANDO AUTENTICAÇÃO
✅ Login válido - Dra. Ana Costa
✅ Login inválido rejeitado
✅ Token válido aceito

📊 RESUMO DOS TESTES
============================================================
Total de testes: 15
Sucessos: 15
Falhas: 0
Taxa de sucesso: 100.0%
🎉 TODOS OS TESTES PASSARAM!
```

## 🤖 Análise de Machine Learning

O sistema inclui análise de risco baseada em ML que avalia:

- 📈 **Frequência de consultas**
- ❌ **Taxa de cancelamentos**
- ⏰ **Tempo desde última consulta**
- 📉 **Tendências de comparecimento**
- 🧠 **Padrões comportamentais**

### Níveis de Risco
- 🔴 **Alto**: Score ≥ 70 (requer atenção imediata)
- 🟡 **Moderado**: Score 40-69 (monitoramento necessário)
- 🟢 **Baixo**: Score < 40 (padrão normal)

## 📁 Estrutura do Projeto

```
blurosiere-backend/
├── 📂 core/                    # Configurações centrais
│   └── database.py
├── 📊 models/                  # Modelos de dados
│   └── models.py
├── 🛫 routers/                 # Endpoints da API
│   ├── auth.py
│   ├── patients.py
│   ├── psychologists.py
│   ├── appointments.py
│   ├── requests.py
│   ├── reports.py
│   └── ml_analysis.py
├── 📝 schemas/                # Validação de dados
│   └── schemas.py
├── ⚙️ services/                # Lógica de negócio
│   ├── auth_service.py
│   ├── ml_service.py
│   └── report_service.py
├── 🐳 Dockerfile               # Container Docker
├── 🐳 docker-compose.yml      # Orquestração
├── ⚙️ config.py                # Configurações
├── 📜 constants.py            # Constantes
├── 🎨 main.py                 # Aplicação principal
├── 🌱 seed_data.py            # Dados iniciais
├── 🧪 test_fixed.py           # Testes automatizados
└── 📦 requirements.txt        # Dependências
```

## 🔧 Troubleshooting

### 🔴 Problemas Comuns

| Erro | Causa | Solução |
|------|-------|----------|
| 500 Internal Server Error | Banco não inicializado | `python seed_data.py` |
| 403 Forbidden | Usuário sem permissão | Login como psicólogo |
| 401 Unauthorized | Token inválido/expirado | Faça login novamente |
| 422 Validation Error | Dados inválidos | Verifique formato dos dados |
| 404 Not Found | Endpoint incorreto | Verifique URL e método HTTP |

### 🔍 Debug

```bash
# Verificar logs
tail -f logs/app.log

# Testar conexão
curl http://localhost:8000/health

# Verificar banco de dados
python -c "from core.database import engine; print(engine.execute('SELECT 1').scalar())"
```

## 🚀 Deploy

### Vercel (Recomendado)

1. Conecte seu repositório ao Vercel
2. Configure as variáveis de ambiente
3. Deploy automático a cada push

### Docker

```bash
# Build da imagem
docker build -t blurosiere-api .

# Execute o container
docker run -p 8000:8000 blurosiere-api
```

### Heroku

```bash
# Login no Heroku
heroku login

# Crie a aplicação
heroku create blurosiere-api

# Configure variáveis
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main
```

## 📊 Monitoramento

- **Health Check**: `/health`
- **Métricas**: `/api/v1/info`
- **Logs**: Estruturados em JSON
- **Alertas**: Configuráveis por ambiente

## 🔒 Segurança

- 🔐 **JWT Authentication**
- 🔒 **Password Hashing** (bcrypt)
- 🚫 **CORS Protection**
- 🛡️ **Input Validation**
- 📝 **Request Logging**
- ⏱️ **Rate Limiting** (configurável)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

- 📚 **Documentação**: http://localhost:8000/docs
- 🐛 **Issues**: [GitHub Issues](https://github.com/LuisSarache/blurosiere-backend/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/LuisSarache/blurosiere-backend/discussions)

---

<div align="center">
  <p>Desenvolvido com ❤️ por <a href="https://github.com/LuisSarache">Luis Sarache</a></p>
  <p>🌹 <strong>Blurosiere</strong> - Cuidando da saúde mental com tecnologia 🌹</p>
</div>