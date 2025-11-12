import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"

# 🎨 Cores para destaque no terminal
class Colors:
    HEADER = "\033[95m" 
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


class TestRunner:
    def __init__(self):
        self.token = None
        self.headers = {}
        self.user = None

    # ----------------------------------
    # LOGIN
    # ----------------------------------
    def login(self):
        print(f"{Colors.HEADER}🔐 Fazendo login...{Colors.RESET}")

        login_data = {"email": "ana@test.com", "password": "123456"}
        try:
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.user = data["user"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
                print(f"{Colors.OKGREEN}✅ Login realizado como: {self.user['name']}{Colors.RESET}")
                return True
            else:
                print(f"{Colors.FAIL}❌ Falha no login ({response.status_code}): {response.text}{Colors.RESET}")
                return False

        except requests.exceptions.ConnectionError:
            print(f"{Colors.FAIL}❌ Servidor não está rodando.{Colors.RESET}")
            return False

    # ----------------------------------
    # MÉTODOS AUXILIARES DE REQUISIÇÃO
    # ----------------------------------
    def get(self, endpoint):
        return requests.get(f"{BASE_URL}{endpoint}", headers=self.headers)

    def post(self, endpoint, data):
        return requests.post(f"{BASE_URL}{endpoint}", json=data, headers=self.headers)

    def put(self, endpoint, data):
        return requests.put(f"{BASE_URL}{endpoint}", json=data, headers=self.headers)

    # ----------------------------------
    # TESTE DE SOLICITAÇÕES
    # ----------------------------------
    def test_requests(self):
        print(f"\n{Colors.OKBLUE}📋 TESTANDO SOLICITAÇÕES (/requests){Colors.RESET}")

        # GET
        response = self.get("/requests")
        if response.status_code == 200:
            requests_data = response.json()
            print(f"{Colors.OKGREEN}✅ Listagem retornou {len(requests_data)} solicitações.{Colors.RESET}")
        elif response.status_code == 403:
            print(f"{Colors.WARNING}⚠️ Usuário não é psicólogo — acesso negado (403).{Colors.RESET}")
        elif response.status_code == 500:
            print(f"{Colors.FAIL}❌ Erro interno do servidor (500). Resposta: {response.text}{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}❌ Erro na listagem ({response.status_code}): {response.text}{Colors.RESET}")

        # POST
        print(f"\n{Colors.OKCYAN}➕ Criando nova solicitação...{Colors.RESET}")
        request_data = {
            "patient_name": "Carlos Teste",
            "patient_email": "carlos@test.com",
            "patient_phone": "11999999999",
            "preferred_psychologist": self.user["id"],
            "description": "Solicitação automática de teste.",
            "preferred_dates": ["2025-11-15", "2025-11-16"],
            "preferred_times": ["09:00", "14:00"],
            "urgency": "media"
        }

        response = self.post("/requests", request_data)
        if response.status_code == 200:
            created_request = response.json()
            print(f"{Colors.OKGREEN}✅ Solicitação criada com ID {created_request['id']}{Colors.RESET}")
        elif response.status_code == 400:
            print(f"{Colors.WARNING}⚠️ Já existe uma solicitação pendente para este psicólogo.{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}❌ Erro ao criar solicitação ({response.status_code}): {response.text}{Colors.RESET}")

        # PUT
        print(f"\n{Colors.OKCYAN}✏️ Atualizando status da solicitação...{Colors.RESET}")
        response = self.get("/requests")
        if response.status_code == 200 and response.json():
            request_id = response.json()[0]["id"]
            update_data = {
                "status": "approved",
                "notes": "Solicitação aprovada automaticamente para testes."
            }
            response = self.put(f"/requests/{request_id}", update_data)
            if response.status_code == 200:
                print(f"{Colors.OKGREEN}✅ Solicitação {request_id} atualizada com sucesso.{Colors.RESET}")
            elif response.status_code == 403:
                print(f"{Colors.WARNING}⚠️ Usuário não é psicólogo — não pode atualizar solicitações.{Colors.RESET}")
            elif response.status_code == 404:
                print(f"{Colors.FAIL}❌ Solicitação não encontrada.{Colors.RESET}")
            else:
                print(f"{Colors.FAIL}❌ Erro ao atualizar ({response.status_code}): {response.text}{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️ Nenhuma solicitação disponível para atualizar.{Colors.RESET}")


    # ----------------------------------
    # EXECUTAR TODOS OS TESTES
    # ----------------------------------
    def run_all_tests(self):
        print(f"{Colors.BOLD}🧪 INICIANDO TESTES DO SISTEMA LUNYSSE{Colors.RESET}")
        print("=" * 60)
        start_time = time.time()

        if not self.login():
            print(f"{Colors.FAIL}❌ Login falhou. Encerrando testes.{Colors.RESET}")
            return False

        self.test_requests()

        print("\n" + "=" * 60)
        print(f"{Colors.OKGREEN}✅ TESTES CONCLUÍDOS COM SUCESSO{Colors.RESET}")
        print(f"⏱️ Tempo total: {round(time.time() - start_time, 2)}s")
        return True


if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)