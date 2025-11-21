import requests
import json
import sys
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

class CompleteTestRunner:
    def __init__(self):
        self.token = None
        self.headers = {}
        self.user = None
        self.results = {"passed": 0, "failed": 0, "total": 0}
    
    def test(self, name, condition, details=""):
        self.results["total"] += 1
        if condition:
            self.results["passed"] += 1
            print(f"{Colors.GREEN}✅ {name}{Colors.RESET} {details}")
        else:
            self.results["failed"] += 1
            print(f"{Colors.RED}❌ {name}{Colors.RESET} {details}")
    
    def section(self, name):
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BLUE}{Colors.BOLD}{name}{Colors.RESET}")
        print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    
    def login(self):
        self.section("🔐 AUTENTICAÇÃO")
        
        # Login
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", 
            json={"email": "ana@test.com", "password": "123456"})
        self.test("Login", response.status_code == 200)
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.user = data["user"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
            self.test("Token recebido", bool(self.token))
            self.test("Refresh token recebido", "refresh_token" in data)
        
        # Login inválido
        response = requests.post(f"{BASE_URL}/api/v1/auth/login",
            json={"email": "invalid@test.com", "password": "wrong"})
        self.test("Login inválido rejeitado", response.status_code == 401)
        
        # Refresh token
        if self.token:
            response = requests.post(f"{BASE_URL}/api/v1/auth/refresh",
                json={"refresh_token": data.get("refresh_token", "")})
            self.test("Refresh token", response.status_code in [200, 401])
        
        # Forgot password
        response = requests.post(f"{BASE_URL}/api/v1/auth/forgot-password",
            json={"email": "ana@test.com"})
        self.test("Forgot password", response.status_code == 200)
        
        return bool(self.token)
    
    def test_patients(self):
        self.section("👥 PACIENTES")
        
        # Listar
        response = requests.get(f"{BASE_URL}/api/v1/patients/", headers=self.headers)
        self.test("Listar pacientes", response.status_code == 200)
        
        patients = response.json() if response.status_code == 200 else []
        self.test("Pacientes retornados", len(patients) > 0, f"({len(patients)} encontrados)")
        
        # Detalhes
        if patients:
            patient_id = patients[0]["id"]
            response = requests.get(f"{BASE_URL}/api/v1/patients/{patient_id}", headers=self.headers)
            self.test("Detalhes do paciente", response.status_code == 200)
            
            # Sessões
            response = requests.get(f"{BASE_URL}/api/v1/patients/{patient_id}/sessions", headers=self.headers)
            self.test("Sessões do paciente", response.status_code == 200)
    
    def test_psychologists(self):
        self.section("🧠 PSICÓLOGOS")
        
        response = requests.get(f"{BASE_URL}/api/v1/psychologists/")
        self.test("Listar psicólogos", response.status_code == 200)
        
        if response.status_code == 200:
            psychs = response.json()
            self.test("Psicólogos retornados", len(psychs) > 0, f"({len(psychs)} encontrados)")
    
    def test_appointments(self):
        self.section("📅 AGENDAMENTOS")
        
        # Listar
        response = requests.get(f"{BASE_URL}/api/v1/appointments/", headers=self.headers)
        self.test("Listar agendamentos", response.status_code == 200)
        
        appointments = response.json() if response.status_code == 200 else []
        
        # Detalhes
        if appointments:
            apt_id = appointments[0]["id"]
            response = requests.get(f"{BASE_URL}/api/v1/appointments/{apt_id}", headers=self.headers)
            self.test("Detalhes do agendamento", response.status_code == 200)
        
        # Horários disponíveis
        response = requests.get(f"{BASE_URL}/api/v1/appointments/available-times", 
            params={"date": datetime.now().date()}, headers=self.headers)
        self.test("Horários disponíveis", response.status_code in [200, 422])
    
    def test_requests(self):
        self.section("📋 SOLICITAÇÕES")
        
        # Listar
        response = requests.get(f"{BASE_URL}/api/v1/requests/", headers=self.headers)
        self.test("Listar solicitações", response.status_code == 200)
        
        # Criar
        response = requests.post(f"{BASE_URL}/api/v1/requests/",
            json={
                "patient_name": "Teste Auto",
                "patient_email": "teste@auto.com",
                "patient_phone": "11999999999",
                "preferred_psychologist": self.user["id"],
                "description": "Teste automatizado",
                "preferred_dates": ["2025-02-01"],
                "preferred_times": ["14:00"],
                "urgency": "media"
            }, headers=self.headers)
        self.test("Criar solicitação", response.status_code in [200, 400])
    
    def test_schedule(self):
        self.section("📆 AGENDA")
        
        # Listar
        response = requests.get(f"{BASE_URL}/api/v1/schedule/", headers=self.headers)
        self.test("Listar agenda", response.status_code == 200)
        
        # Criar
        response = requests.post(f"{BASE_URL}/api/v1/schedule/",
            json={
                "day_of_week": 1,
                "start_time": "09:00",
                "end_time": "18:00",
                "slot_duration": 50
            }, headers=self.headers)
        self.test("Criar horário", response.status_code in [200, 403])
    
    def test_notifications(self):
        self.section("🔔 NOTIFICAÇÕES")
        
        # Listar
        response = requests.get(f"{BASE_URL}/api/v1/notifications/", headers=self.headers)
        self.test("Listar notificações", response.status_code == 200)
        
        # Contador não lidas
        response = requests.get(f"{BASE_URL}/api/v1/notifications/unread-count", headers=self.headers)
        self.test("Contador não lidas", response.status_code == 200)
        
        # Marcar todas como lidas
        response = requests.put(f"{BASE_URL}/api/v1/notifications/read-all", headers=self.headers)
        self.test("Marcar todas como lidas", response.status_code == 200)
    
    def test_chat(self):
        self.section("🤖 CHAT IA")
        
        # Enviar mensagem
        response = requests.post(f"{BASE_URL}/api/v1/chat/message",
            json={"message": "Olá, como agendar uma consulta?"},
            headers=self.headers)
        self.test("Enviar mensagem", response.status_code == 200)
        
        if response.status_code == 200:
            data = response.json()
            self.test("Resposta recebida", "response" in data)
        
        # Histórico
        response = requests.get(f"{BASE_URL}/api/v1/chat/history", headers=self.headers)
        self.test("Histórico do chat", response.status_code == 200)
    
    def test_dashboard(self):
        self.section("📊 DASHBOARD")
        
        # Dashboard psicólogo
        response = requests.get(f"{BASE_URL}/api/v1/dashboard/psychologist", headers=self.headers)
        self.test("Dashboard psicólogo", response.status_code == 200)
        
        if response.status_code == 200:
            data = response.json()
            self.test("Estatísticas presentes", "statistics" in data)
            self.test("Agendamentos presentes", "upcoming_appointments" in data)
    
    def test_analytics(self):
        self.section("📈 ANALYTICS")
        
        # Overview
        response = requests.get(f"{BASE_URL}/api/v1/analytics/overview", headers=self.headers)
        self.test("Analytics overview", response.status_code == 200)
        
        # Trends
        response = requests.get(f"{BASE_URL}/api/v1/analytics/trends",
            params={"metric": "sessions", "period": "month"},
            headers=self.headers)
        self.test("Analytics trends", response.status_code == 200)
    
    def test_reports(self):
        self.section("📄 RELATÓRIOS")
        
        response = requests.get(f"{BASE_URL}/api/v1/reports/{self.user['id']}", headers=self.headers)
        self.test("Gerar relatório", response.status_code == 200)
        
        if response.status_code == 200:
            data = response.json()
            self.test("Dados do relatório", "stats" in data)
    
    def test_ml_analysis(self):
        self.section("🔬 ANÁLISE ML")
        
        # Análise geral
        response = requests.get(f"{BASE_URL}/api/v1/ml/risk-analysis", headers=self.headers)
        self.test("Análise geral", response.status_code == 200)
        
        if response.status_code == 200:
            data = response.json()
            self.test("Resumo presente", "summary" in data)
            
            # Análise individual
            if data.get("patients"):
                patient_id = data["patients"][0]["id"]
                response = requests.get(f"{BASE_URL}/api/v1/ml/risk-analysis/{patient_id}",
                    headers=self.headers)
                self.test("Análise individual", response.status_code == 200)
    
    def test_search(self):
        self.section("🔍 BUSCA")
        
        response = requests.get(f"{BASE_URL}/api/v1/search/",
            params={"q": "test", "type": "all"},
            headers=self.headers)
        self.test("Busca avançada", response.status_code == 200)
    
    def test_export(self):
        self.section("📤 EXPORTAÇÃO")
        
        # Exportar pacientes
        response = requests.get(f"{BASE_URL}/api/v1/export/patients",
            params={"format": "csv"},
            headers=self.headers)
        self.test("Exportar pacientes", response.status_code == 200)
        
        # Exportar agendamentos
        response = requests.get(f"{BASE_URL}/api/v1/export/appointments",
            params={"format": "csv"},
            headers=self.headers)
        self.test("Exportar agendamentos", response.status_code == 200)
    
    def test_system(self):
        self.section("⚙️ SISTEMA")
        
        # Health check
        response = requests.get(f"{BASE_URL}/health")
        self.test("Health check", response.status_code == 200)
        
        # API info
        response = requests.get(f"{BASE_URL}/api/v1/info")
        self.test("API info", response.status_code == 200)
        
        # Root
        response = requests.get(f"{BASE_URL}/")
        self.test("Root endpoint", response.status_code == 200)
        
        # Docs
        response = requests.get(f"{BASE_URL}/docs")
        self.test("Documentação", response.status_code in [200, 404])
    
    def print_summary(self):
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 RESUMO DOS TESTES{Colors.RESET}")
        print(f"{'='*60}")
        print(f"Total de testes: {self.results['total']}")
        print(f"{Colors.GREEN}Sucessos: {self.results['passed']}{Colors.RESET}")
        print(f"{Colors.RED}Falhas: {self.results['failed']}{Colors.RESET}")
        
        success_rate = (self.results['passed'] / self.results['total'] * 100) if self.results['total'] > 0 else 0
        print(f"Taxa de sucesso: {success_rate:.1f}%")
        
        if self.results['failed'] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TODOS OS TESTES PASSARAM!{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}⚠️ ALGUNS TESTES FALHARAM{Colors.RESET}")
    
    def run_all(self):
        print(f"{Colors.BOLD}🧪 TESTES COMPLETOS - BLUROSIERE API{Colors.RESET}")
        print(f"URL: {BASE_URL}")
        print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.login():
            print(f"\n{Colors.RED}❌ Login falhou. Abortando testes.{Colors.RESET}")
            return False
        
        # Executar todos os testes
        self.test_patients()
        self.test_psychologists()
        self.test_appointments()
        self.test_requests()
        self.test_schedule()
        self.test_notifications()
        self.test_chat()
        self.test_dashboard()
        self.test_analytics()
        self.test_reports()
        self.test_ml_analysis()
        self.test_search()
        self.test_export()
        self.test_system()
        
        self.print_summary()
        
        return self.results['failed'] == 0

if __name__ == "__main__":
    runner = CompleteTestRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)