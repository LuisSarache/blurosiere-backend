# 🧪 Guia de Testes - BluRosiere Backend

## 📋 Visão Geral

Este documento descreve como executar e criar testes para o sistema.

---

## 🚀 Executando Testes

### Método 1: Script Completo (Recomendado)

```bash
python run_tests.py
```

Executa:
- ✅ Testes de integração (todos os endpoints)
- ✅ Testes unitários (pytest)

### Método 2: Testes de Integração

```bash
python test_complete.py
```

Testa todos os endpoints da API em sequência.

### Método 3: Testes Unitários

```bash
pytest tests/ -v
```

Executa testes unitários com pytest.

### Método 4: Teste Específico

```bash
pytest tests/test_auth.py -v
```

---

## 📊 Cobertura de Testes

### Endpoints Testados (100%)

#### Autenticação
- ✅ POST /api/v1/auth/login
- ✅ POST /api/v1/auth/refresh
- ✅ POST /api/v1/auth/logout
- ✅ POST /api/v1/auth/forgot-password

#### Pacientes
- ✅ GET /api/v1/patients/
- ✅ GET /api/v1/patients/{id}
- ✅ GET /api/v1/patients/{id}/sessions

#### Psicólogos
- ✅ GET /api/v1/psychologists/

#### Agendamentos
- ✅ GET /api/v1/appointments/
- ✅ GET /api/v1/appointments/{id}
- ✅ GET /api/v1/appointments/available-times

#### Solicitações
- ✅ GET /api/v1/requests/
- ✅ POST /api/v1/requests/

#### Agenda
- ✅ GET /api/v1/schedule/
- ✅ POST /api/v1/schedule/

#### Notificações
- ✅ GET /api/v1/notifications/
- ✅ GET /api/v1/notifications/unread-count
- ✅ PUT /api/v1/notifications/read-all

#### Chat IA
- ✅ POST /api/v1/chat/message
- ✅ GET /api/v1/chat/history

#### Dashboard
- ✅ GET /api/v1/dashboard/psychologist
- ✅ GET /api/v1/dashboard/patient

#### Analytics
- ✅ GET /api/v1/analytics/overview
- ✅ GET /api/v1/analytics/trends

#### Relatórios
- ✅ GET /api/v1/reports/{id}

#### Análise ML
- ✅ GET /api/v1/ml/risk-analysis
- ✅ GET /api/v1/ml/risk-analysis/{id}

#### Busca
- ✅ GET /api/v1/search/

#### Exportação
- ✅ GET /api/v1/export/patients
- ✅ GET /api/v1/export/appointments

#### Sistema
- ✅ GET /health
- ✅ GET /api/v1/info
- ✅ GET /

---

## 🔧 Configuração de Testes

### Pré-requisitos

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Inicializar banco de dados de teste
python seed_data.py
```

### Variáveis de Ambiente

```env
# .env.test
DATABASE_URL=sqlite:///./test.db
DEBUG=True
SECRET_KEY=test-secret-key
```

---

## 📝 Criando Novos Testes

### Teste de Integração

```python
# test_complete.py
def test_new_endpoint(self):
    self.section("🆕 NOVO ENDPOINT")
    
    response = requests.get(f"{BASE_URL}/api/v1/new-endpoint",
        headers=self.headers)
    self.test("Novo endpoint", response.status_code == 200)
```

### Teste Unitário

```python
# tests/test_new_feature.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_new_feature():
    response = client.get("/api/v1/new-endpoint")
    assert response.status_code == 200
    assert "data" in response.json()
```

---

## 🎯 Boas Práticas

### 1. Sempre Teste Antes de Commit

```bash
python run_tests.py
git commit -m "feat: nova funcionalidade"
```

### 2. Teste Casos de Erro

```python
def test_invalid_input():
    response = client.post("/api/v1/endpoint", json={})
    assert response.status_code == 422
```

### 3. Use Fixtures

```python
@pytest.fixture
def auth_headers():
    # Setup
    token = get_test_token()
    return {"Authorization": f"Bearer {token}"}
```

### 4. Teste Isolado

```python
def test_isolated():
    # Cada teste deve ser independente
    # Não dependa de ordem de execução
    pass
```

---

## 📊 Resultados Esperados

### Testes de Integração

```
🧪 TESTES COMPLETOS - BLUROSIERE API
============================================================
🔐 AUTENTICAÇÃO
✅ Login
✅ Token recebido
✅ Refresh token recebido
✅ Login inválido rejeitado

... (todos os endpoints)

📊 RESUMO DOS TESTES
============================================================
Total de testes: 50+
Sucessos: 50+
Falhas: 0
Taxa de sucesso: 100.0%
🎉 TODOS OS TESTES PASSARAM!
```

### Testes Unitários

```
tests/test_auth.py::test_login_success PASSED
tests/test_auth.py::test_login_invalid PASSED
tests/test_endpoints.py::test_patients_list PASSED
...

========== 20 passed in 5.23s ==========
```

---

## 🐛 Troubleshooting

### Servidor não está rodando

```bash
# Terminal 1: Iniciar servidor
python main.py

# Terminal 2: Executar testes
python test_complete.py
```

### Banco de dados vazio

```bash
python seed_data.py
```

### Testes falhando

```bash
# Ver logs detalhados
pytest tests/ -v -s

# Ver apenas falhas
pytest tests/ --tb=short
```

### Limpar cache

```bash
# Pytest cache
pytest --cache-clear

# Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
```

---

## 📈 CI/CD

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python seed_data.py
      - run: python run_tests.py
```

---

## 📞 Suporte

Para dúvidas sobre testes:
- 📧 Email: tests@blurosiere.com
- 📖 Docs: [Documentação Completa](./README.md)

---

**BluRosiere Testing Guide v2.0.0**  
Testes completos para sistema enterprise-grade