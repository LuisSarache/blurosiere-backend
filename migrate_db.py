"""
Script para atualizar o banco de dados com os novos modelos
"""
from core.database import engine, Base
from models.models import *
from models.refresh_token import RefreshToken

def migrate():
    print("Atualizando banco de dados...")
    try:
        # Cria todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("Banco de dados atualizado com sucesso!")
        print("\nTabelas criadas/atualizadas:")
        print("  - users")
        print("  - patients")
        print("  - appointments")
        print("  - requests")
        print("  - schedules")
        print("  - notifications")
        print("  - chat_messages")
        print("  - audit_logs")
        print("  - reports")
        print("  - refresh_tokens")
    except Exception as e:
        print(f"❌ Erro ao atualizar banco: {e}")
        raise

if __name__ == "__main__":
    migrate()