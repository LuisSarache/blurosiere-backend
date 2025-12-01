# 🔗 Guia de Integração Frontend-Backend

## 📋 Configuração Inicial

### 1. Backend (já configurado)
```bash
# O backend está rodando em:
http://localhost:8000

# Documentação da API:
http://localhost:8000/docs
```

### 2. Frontend - Configuração

#### Criar arquivo `.env` no frontend:
```env
VITE_API_URL=http://localhost:8000/api/v1
# ou para React:
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 🔐 Autenticação

### Login
```javascript
// api/auth.js
const API_URL = import.meta.env.VITE_API_URL; // Vite
// const API_URL = process.env.REACT_APP_API_URL; // React

export const login = async (email, password) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (!response.ok) throw new Error('Login falhou');
  
  const data = await response.json();
  // Salvar token
  localStorage.setItem('token', data.access_token);
  localStorage.setItem('user', JSON.stringify(data.user));
  
  return data;
};
```

### Registro
```javascript
export const register = async (userData) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  
  if (!response.ok) throw new Error('Registro falhou');
  return response.json();
};
```

## 🛡️ Requisições Autenticadas

### Helper para requisições com token
```javascript
// api/client.js
const API_URL = import.meta.env.VITE_API_URL;

export const apiClient = async (endpoint, options = {}) => {
  const token = localStorage.getItem('token');
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
  };
  
  const response = await fetch(`${API_URL}${endpoint}`, config);
  
  if (response.status === 401) {
    // Token expirado - redirecionar para login
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
    throw new Error('Sessão expirada');
  }
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Erro na requisição');
  }
  
  return response.json();
};
```

## 📊 Exemplos de Uso

### Pacientes
```javascript
// api/patients.js
import { apiClient } from './client';

// Listar pacientes
export const getPatients = () => apiClient('/patients/');

// Detalhes do paciente
export const getPatient = (id) => apiClient(`/patients/${id}`);

// Criar paciente
export const createPatient = (data) => 
  apiClient('/patients/', {
    method: 'POST',
    body: JSON.stringify(data)
  });

// Sessões do paciente
export const getPatientSessions = (id) => 
  apiClient(`/patients/${id}/sessions`);
```

### Agendamentos
```javascript
// api/appointments.js
import { apiClient } from './client';

// Listar agendamentos
export const getAppointments = () => apiClient('/appointments/');

// Criar agendamento
export const createAppointment = (data) =>
  apiClient('/appointments/', {
    method: 'POST',
    body: JSON.stringify(data)
  });

// Horários disponíveis
export const getAvailableTimes = (date) =>
  apiClient(`/appointments/available-times?date=${date}`);

// Cancelar agendamento
export const cancelAppointment = (id) =>
  apiClient(`/appointments/${id}`, { method: 'DELETE' });
```

### Dashboard
```javascript
// api/dashboard.js
import { apiClient } from './client';

// Dashboard do psicólogo
export const getPsychologistDashboard = () =>
  apiClient('/dashboard/psychologist');

// Dashboard do paciente
export const getPatientDashboard = () =>
  apiClient('/dashboard/patient');
```

## 🎨 Exemplo Completo - React Component

```jsx
// components/PatientList.jsx
import { useState, useEffect } from 'react';
import { getPatients } from '../api/patients';

export default function PatientList() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    try {
      setLoading(true);
      const data = await getPatients();
      setPatients(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;

  return (
    <div>
      <h2>Pacientes</h2>
      <ul>
        {patients.map(patient => (
          <li key={patient.id}>
            {patient.name} - {patient.email}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## 🔄 Context API para Autenticação (React)

```jsx
// context/AuthContext.jsx
import { createContext, useState, useContext, useEffect } from 'react';
import { login as apiLogin } from '../api/auth';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const data = await apiLogin(email, password);
    setUser(data.user);
    return data;
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

## 📱 Axios (Alternativa ao Fetch)

```javascript
// api/axios.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' }
});

// Interceptor para adicionar token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para tratar erros
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Uso:
// import api from './api/axios';
// const patients = await api.get('/patients/');
```

## 🧪 Testar Conexão

```javascript
// test-connection.js
const API_URL = 'http://localhost:8000';

async function testConnection() {
  try {
    // 1. Testar servidor
    const health = await fetch(`${API_URL}/health`);
    console.log('✅ Servidor:', await health.json());

    // 2. Testar login
    const login = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'ana@test.com',
        password: '123456'
      })
    });
    const loginData = await login.json();
    console.log('✅ Login:', loginData.user.name);

    // 3. Testar endpoint autenticado
    const patients = await fetch(`${API_URL}/api/v1/patients/`, {
      headers: { 'Authorization': `Bearer ${loginData.access_token}` }
    });
    console.log('✅ Pacientes:', await patients.json());

  } catch (error) {
    console.error('❌ Erro:', error);
  }
}

testConnection();
```

## 🚀 Checklist de Integração

- [ ] Backend rodando em `http://localhost:8000`
- [ ] CORS configurado no `.env` do backend
- [ ] Variável `VITE_API_URL` ou `REACT_APP_API_URL` no frontend
- [ ] Helper de API criado (`apiClient` ou `axios`)
- [ ] Sistema de autenticação implementado
- [ ] Token sendo enviado nas requisições
- [ ] Tratamento de erros 401 (token expirado)
- [ ] Teste de conexão funcionando

## 📞 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/auth/login` | Login |
| POST | `/auth/register` | Registro |
| GET | `/patients/` | Listar pacientes |
| POST | `/patients/` | Criar paciente |
| GET | `/appointments/` | Listar agendamentos |
| POST | `/appointments/` | Criar agendamento |
| GET | `/appointments/available-times` | Horários disponíveis |
| GET | `/psychologists/` | Listar psicólogos |
| GET | `/dashboard/psychologist` | Dashboard psicólogo |
| GET | `/notifications/` | Notificações |

## 🐛 Troubleshooting

### CORS Error
```bash
# Adicione a URL do frontend no .env do backend:
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 401 Unauthorized
- Verifique se o token está sendo enviado
- Verifique se o token não expirou
- Faça login novamente

### Network Error
- Verifique se o backend está rodando
- Verifique a URL da API no `.env`
- Teste com `curl http://localhost:8000/health`

## 📚 Documentação Completa

Acesse: http://localhost:8000/docs
