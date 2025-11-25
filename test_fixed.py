#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de testes automatizados para Blurosiere API
Testa todos os endpoints principais e funcionalidades
"""

import requests
import json
import sys
import time
from datetime import datetime, timedelta
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
            print(f"{Colors.GREEN}[OK] {test_name}{Colors.RESET} {details}")
        else:
            self.test_results["failed"] += 1
            print(f"{Colors.RED}[FAIL] {test_name}{Colors.RESET} {details}")
    
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
        print(f"\n{Colors.HEADER}TESTANDO SAUDE DO SERVIDOR{Colors.RESET}")
        
        try:
            response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
            self.log_test("Servidor rodando", response.status_code == 200)
            
            response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
            self.log_test("Health check", response.status_code == 200)
            
            response = requests.get(f"{BASE_URL}{API_PREFIX}/info", timeout=TIMEOUT)
            self.log_test("API info", response.status_code == 200)
            
            return True
        except requests.exceptions.ConnectionError:
            self.log_test("Conexão com servidor", False, "- Servidor não está rodando")
            return False
    
    def test_authentication(self) -> bool:
        """Testa sistema de autenticação"""
        print(f"\n{Colors.HEADER}TESTANDO AUTENTICACAO{Colors.RESET}")
        
        login_data = {"email": "ana@test.com", "password": "123456"}
        response = self.make_request("POST", "/auth/login", json=login_data)
        
        if response and response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.user = data["user"]
            self.headers["Authorization"] = f"Bearer {self.token}"
            self.log_test("Login válido", True, f"- {self.user['name']}")
        else:
            self.log_test("Login válido", False)
            return False
        
        invalid_login = {"email": "invalid@test.com", "password": "wrong"}
        response = self.make_request("POST", "/auth/login", json=invalid_login)
        expected_status = response and response.status_code == 401
        if not expected_status and response:
            details = f"- Status: {response.status_code}"
        else:
            details = ""
        self.log_test("Login inválido rejeitado", expected_status, details)
        
        response = self.make_request("GET", "/patients/")
        self.log_test("Token válido aceito", response and response.status_code == 200)
        
        return True
    
    def test_patients_endpoint(self):
        """Testa endpoints de pacientes"""
        print(f"\n{Colors.BLUE}TESTANDO PACIENTES{Colors.RESET}")
        
        response = self.make_request("GET", "/patients/")
        if response and response.status_code == 200:
            patients = response.json()
            self.log_test("Listagem de pacientes", True, f"- {len(patients)} encontrados")
            
            if patients:
                patient_id = patients[0]["id"]
                response = self.make_request("GET", f"/patients/{patient_id}")
                self.log_test("Detalhes do paciente", response and response.status_code == 200)
                
                response = self.make_request("GET", f"/patients/{patient_id}/sessions")
                self.log_test("Sessões do paciente", response and response.status_code == 200)
        else:
            self.log_test("Listagem de pacientes", False)
    
    def test_psychologists_endpoint(self):
        """Testa endpoints de psicólogos"""
        print(f"\n{Colors.BLUE}TESTANDO PSICOLOGOS{Colors.RESET}")
        
        response = self.make_request("GET", "/psychologists/")
        if response and response.status_code == 200:
            psychologists = response.json()
            self.log_test("Listagem de psicólogos", True, f"- {len(psychologists)} encontrados")
        else:
            self.log_test("Listagem de psicólogos", False)
    
    def test_appointments_endpoint(self):
        """Testa endpoints de agendamentos"""
        print(f"\n{Colors.CYAN}TESTANDO AGENDAMENTOS{Colors.RESET}")
        
        response = self.make_request("GET", "/appointments/")
        if response and response.status_code == 200:
            appointments = response.json()
            self.log_test("Listagem de agendamentos", True, f"- {len(appointments)} encontrados")
            
            if appointments:
                apt_id = appointments[0]["id"]
                response = self.make_request("GET", f"/appointments/{apt_id}")
                self.log_test("Detalhes do agendamento", response and response.status_code == 200)
        else:
            self.log_test("Listagem de agendamentos", False)
        
        # Test available times with date parameter
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.make_request("GET", f"/appointments/available-times?date={tomorrow}")
        self.log_test("Horários disponíveis", response and response.status_code == 200)
    
    def test_requests_endpoint(self):
        """Testa endpoints de solicitações"""
        print(f"\n{Colors.CYAN}TESTANDO SOLICITACOES{Colors.RESET}")
        
        response = self.make_request("GET", "/requests/")
        if response and response.status_code == 200:
            requests_data = response.json()
            self.log_test("Listagem de solicitações", True, f"- {len(requests_data)} encontradas")
        else:
            self.log_test("Listagem de solicitações", False)
    
    def test_reports_endpoint(self):
        """Testa endpoints de relatórios"""
        print(f"\n{Colors.YELLOW}TESTANDO RELATORIOS{Colors.RESET}")
        
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
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.HEADER}INICIANDO TESTES - BLUROSIERE API{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
        
        if not self.test_server_health():
            print(f"\n{Colors.RED}Servidor nao esta rodando. Inicie com: python main.py{Colors.RESET}")
            return False
        
        if not self.test_authentication():
            print(f"\n{Colors.RED}Falha na autenticacao{Colors.RESET}")
            return False
        
        self.test_patients_endpoint()
        self.test_psychologists_endpoint()
        self.test_appointments_endpoint()
        self.test_requests_endpoint()
        self.test_reports_endpoint()
        
        self.print_summary()
        return self.test_results["failed"] == 0
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        elapsed = time.time() - self.start_time
        success_rate = (self.test_results["passed"] / self.test_results["total"] * 100) if self.test_results["total"] > 0 else 0
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.HEADER}RESUMO DOS TESTES{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"Total de testes: {self.test_results['total']}")
        print(f"{Colors.GREEN}Sucessos: {self.test_results['passed']}{Colors.RESET}")
        print(f"{Colors.RED}Falhas: {self.test_results['failed']}{Colors.RESET}")
        print(f"Taxa de sucesso: {success_rate:.1f}%")
        print(f"Tempo: {elapsed:.2f}s")
        
        if self.test_results["failed"] == 0:
            print(f"\n{Colors.GREEN}TODOS OS TESTES PASSARAM!{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}ALGUNS TESTES FALHARAM{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")

if __name__ == "__main__":
    runner = APITestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)
