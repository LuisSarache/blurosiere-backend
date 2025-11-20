#!/usr/bin/env python3
"""
Suite de testes automatizados para Blurosiere API
Testa todos os endpoints principais e funcionalidades
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Configurações
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"
TIMEOUT = 10

class Colors:
    """Cores para output no terminal"""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

class APITestRunner:
    """Executor de testes da API Blurosiere"""
    
    def __init__(self):
        self.token: Optional[str] = None
        self.headers: Dict[str, str] = {}
        self.user: Optional[Dict[str, Any]] = None
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "total": 0
        }
        self.start_time = time.time()
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Registra resultado de um teste"""
        self.test_results["total"] += 1
        if passed:
            self.test_results["passed"] += 1
            print(f"{Colors.GREEN}✅ {test_name}{Colors.RESET} {details}")
        else:
            self.test_results["failed"] += 1
            print(f"{Colors.RED}❌ {test_name}{Colors.RESET} {details}")
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Faz requisição HTTP com tratamento de erro"""
        url = f"{BASE_URL}{API_PREFIX}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=TIMEOUT,
                headers=self.headers,
                **kwargs
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}Erro de conexão: {e}{Colors.RESET}")
            return None
    
    def test_server_health(self) -> bool:
        """Testa se o servidor está rodando"""
        print(f"\n{Colors.HEADER}🏥 TESTANDO SAÚDE DO SERVIDOR{Colors.RESET}")
        
        try:
            # Testa endpoint raiz
            response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
            self.log_test("Servidor rodando", response.status_code == 200)
            
            # Testa health check
            response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
            self.log_test("Health check", response.status_code == 200)
            
            # Testa info da API
            response = requests.get(f"{BASE_URL}{API_PREFIX}/info", timeout=TIMEOUT)
            self.log_test("API info", response.status_code == 200)
            
            return True
        except requests.exceptions.ConnectionError:
            self.log_test("Conexão com servidor", False, "- Servidor não está rodando")
            return False
    
    def test_authentication(self) -> bool:
        """Testa sistema de autenticação"""
        print(f"\n{Colors.HEADER}🔐 TESTANDO AUTENTICAÇÃO{Colors.RESET}")
        
        # Teste 1: Login válido
        login_data = {"email": "ana@test.com", "password": "123456"}
        response = self.make_request("POST", "/auth/login", json=login_data)
        
        if response and response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.user = data["user"]
            self.headers["Authorization"] = f"Bearer {self.token}"
            self.log_test("Login válido", True, f"- {self.user['name']}")
        else:
            self.log_test("Login válido", False, f"- Status: {response.status_code if response else 'N/A'}")
            return False
        
        # Teste 2: Login inválido
        invalid_login = {"email": "invalid@test.com", "password": "wrong"}
        response = self.make_request("POST", "/auth/login", json=invalid_login)
        self.log_test("Login inválido rejeitado", response and response.status_code == 401)
        
        # Teste 3: Acesso com token válido
        response = self.make_request("GET", "/patients/")
        self.log_test("Token válido aceito", response and response.status_code == 200)
        
        return True
    
    def test_patients_endpoint(self):
        """Testa endpoints de pacientes"""
        print(f"\n{Colors.BLUE}👥 TESTANDO PACIENTES{Colors.RESET}")
        
        # Listar pacientes
        response = self.make_request("GET", "/patients/")
        if response and response.status_code == 200:
            patients = response.json()
            self.log_test("Listagem de pacientes", True, f"- {len(patients)} encontrados")
            
            # Testar detalhes se houver pacientes
            if patients:
                patient_id = patients[0]["id"]
                response = self.make_request("GET", f"/patients/{patient_id}")
                self.log_test("Detalhes do paciente", response and response.status_code == 200)
                
                # Testar sessões do paciente
                response = self.make_request("GET", f"/patients/{patient_id}/sessions")
                self.log_test("Sessões do paciente", response and response.status_code == 200)
        else:
            self.log_test("Listagem de pacientes", False)
    
    def test_psychologists_endpoint(self):
        """Testa endpoints de psicólogos"""
        print(f"\n{Colors.BLUE}🧠 TESTANDO PSICÓLOGOS{Colors.RESET}")
        
        response = self.make_request("GET", "/psychologists/")
        if response and response.status_code == 200:
            psychologists = response.json()
            self.log_test("Listagem de psicólogos", True, f"- {len(psychologists)} encontrados")
        else:
            self.log_test("Listagem de psicólogos", False)
    
    def test_appointments_endpoint(self):
        """Testa endpoints de agendamentos"""
        print(f"\n{Colors.CYAN}📅 TESTANDO AGENDAMENTOS{Colors.RESET}")
        
        # Listar agendamentos
        response = self.make_request("GET", "/appointments/")
        if response and response.status_code == 200:
            appointments = response.json()
            self.log_test("Listagem de agendamentos", True, f"- {len(appointments)} encontrados")
            
            # Testar detalhes se houver agendamentos
            if appointments:
                apt_id = appointments[0]["id"]
                response = self.make_request("GET", f"/appointments/{apt_id}")
                self.log_test("Detalhes do agendamento", response and response.status_code == 200)
        else:
            self.log_test("Listagem de agendamentos", False)
        
        # Testar horários disponíveis
        response = self.make_request("GET", "/appointments/available-times")
        self.log_test("Horários disponíveis", response and response.status_code == 200)
    
    def test_requests_endpoint(self):
        """Testa endpoints de solicitações"""
        print(f"\n{Colors.CYAN}📋 TESTANDO SOLICITAÇÕES{Colors.RESET}")
        
        # Listar solicitações
        response = self.make_request("GET", "/requests/")
        if response and response.status_code == 200:
            requests_data = response.json()
            self.log_test("Listagem de solicitações", True, f"- {len(requests_data)} encontradas")
        else:
            self.log_test("Listagem de solicitações", False)
        
        # Testar criação de solicitação
        new_request = {
            "patient_name": "Teste Automatizado",
            "patient_email": "teste@automatizado.com",
            "patient_phone": "11999999999",
            "preferred_psychologist": self.user["id"] if self.user else 2,
            "description": "Solicitação criada por teste automatizado",
            "preferred_dates": ["2025-01-20", "2025-01-21"],
            "preferred_times": ["09:00", "14:00"],
            "urgency": "media"
        }
        
        response = self.make_request("POST", "/requests/", json=new_request)
        self.log_test("Criação de solicitação", response and response.status_code in [200, 201, 400])
    
    def test_reports_endpoint(self):
        """Testa endpoints de relatórios"""
        print(f"\n{Colors.YELLOW}📊 TESTANDO RELATÓRIOS{Colors.RESET}")
        
        if not self.user:
            self.log_test("Relatórios", False, "- Usuário não autenticado")
            return
        
        response = self.make_request("GET", f"/reports/{self.user['id']}")
        if response and response.status_code == 200:
            report = response.json()
            if "stats" in report:
                stats = report["stats"]
                self.log_test("Geração de relatório", True, 
                    f"- {stats.get('active_patients', 0)} pacientes ativos")
            else:
                self.log_test("Geração de relatório", True)
        else:
            self.log_test("Geração de relatório", False)
    
    def test_ml_analysis_endpoint(self):
        """Testa endpoints de análise ML"""
        print(f"\n{Colors.YELLOW}🤖 TESTANDO ANÁLISE ML{Colors.RESET}")
        
        # Análise geral de risco
        response = self.make_request("GET", "/ml/risk-analysis")
        if response and response.status_code == 200:
            data = response.json()
            if "summary" in data:
                summary = data["summary"]
                total = summary.get("total_patients", 0)
                self.log_test("Análise geral de risco", True, f"- {total} pacientes analisados")
                
                # Testar análise individual se houver pacientes
                if "patients" in data and data["patients"]:
                    patient_id = data["patients"][0]["id"]
                    response = self.make_request("GET", f"/ml/risk-analysis/{patient_id}")
                    self.log_test("Análise individual de risco", response and response.status_code == 200)
            else:
                self.log_test("Análise geral de risco", True)
        else:
            self.log_test("Análise geral de risco", False)
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        duration = time.time() - self.start_time
        total = self.test_results["total"]
        passed = self.test_results["passed"]
        failed = self.test_results["failed"]
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 RESUMO DOS TESTES{Colors.RESET}")
        print(f"{'='*60}")
        print(f"Total de testes: {total}")
        print(f"{Colors.GREEN}Sucessos: {passed}{Colors.RESET}")
        print(f"{Colors.RED}Falhas: {failed}{Colors.RESET}")
        print(f"Taxa de sucesso: {success_rate:.1f}%")
        print(f"Tempo de execução: {duration:.2f}s")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TODOS OS TESTES PASSARAM!{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}⚠️  ALGUNS TESTES FALHARAM{Colors.RESET}")
    
    def run_all_tests(self) -> bool:
        """Executa todos os testes"""
        print(f"{Colors.BOLD}🧪 INICIANDO TESTES AUTOMATIZADOS - BLUROSIERE API{Colors.RESET}")
        print(f"{'='*60}")
        print(f"URL Base: {BASE_URL}")
        print(f"Timeout: {TIMEOUT}s")
        print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Executa testes em ordem
        if not self.test_server_health():
            print(f"\n{Colors.RED}❌ Servidor não está acessível. Abortando testes.{Colors.RESET}")
            return False
        
        if not self.test_authentication():
            print(f"\n{Colors.RED}❌ Falha na autenticação. Abortando testes.{Colors.RESET}")
            return False
        
        # Continua com outros testes
        self.test_patients_endpoint()
        self.test_psychologists_endpoint()
        self.test_appointments_endpoint()
        self.test_requests_endpoint()
        self.test_reports_endpoint()
        self.test_ml_analysis_endpoint()
        
        # Imprime resumo
        self.print_summary()
        
        return self.test_results["failed"] == 0

def main():
    """Função principal"""
    runner = APITestRunner()
    success = runner.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())