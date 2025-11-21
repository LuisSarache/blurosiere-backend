import os
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from core.database import engine, Base
from routers import (
    auth, patients, psychologists, appointments, reports, requests, ml_analysis,
    schedule, notifications, chat, dashboard, analytics, search, export, upload, websocket
)
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    logger.info("Iniciando aplicação Blurosiere API")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Encerrando aplicação Blurosiere API")

# Configuração da aplicação
app = FastAPI(
    title=os.getenv("APP_NAME", "Blurosiere API"),
    description="Sistema completo de agendamento psicológico com análise de risco ML",
    version=os.getenv("APP_VERSION", "1.0.0"),
    docs_url="/docs" if os.getenv("DEBUG", "False").lower() == "true" else None,
    redoc_url="/redoc" if os.getenv("DEBUG", "False").lower() == "true" else None,
    lifespan=lifespan
)

# Middleware de segurança
if os.getenv("DEBUG", "False").lower() != "true":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.vercel.app"]
    )

# Configuração CORS
cors_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Tratamento global de exceções
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Inclui os routers com prefixos organizados
app.include_router(auth.router, prefix="/api/v1", tags=["Autenticação"])
app.include_router(patients.router, prefix="/api/v1", tags=["Pacientes"])
app.include_router(psychologists.router, prefix="/api/v1", tags=["Psicólogos"])
app.include_router(appointments.router, prefix="/api/v1", tags=["Agendamentos"])
app.include_router(requests.router, prefix="/api/v1", tags=["Solicitações"])
app.include_router(reports.router, prefix="/api/v1", tags=["Relatórios"])
app.include_router(ml_analysis.router, prefix="/api/v1", tags=["Análise ML"])
app.include_router(schedule.router, prefix="/api/v1", tags=["Agenda"])
app.include_router(notifications.router, prefix="/api/v1", tags=["Notificações"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat IA"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(search.router, prefix="/api/v1", tags=["Busca"])
app.include_router(export.router, prefix="/api/v1", tags=["Exportação"])
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(websocket.router, tags=["WebSocket"])

# Endpoints principais
@app.get("/", tags=["Sistema"])
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "Blurosiere API - Sistema de Agendamento Psicológico",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "docs": "/docs" if os.getenv("DEBUG", "False").lower() == "true" else "Documentação desabilitada em produção"
    }

@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verificação de saúde da API"""
    try:
        # Testa conexão com banco
        from core.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": str(datetime.now())
        }
    except Exception as e:
        logger.error(f"Health check falhou: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )

@app.get("/api/v1/info", tags=["Sistema"])
async def api_info():
    """Informações da API"""
    return {
        "name": os.getenv("APP_NAME", "Blurosiere API"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": "development" if os.getenv("DEBUG", "False").lower() == "true" else "production",
        "endpoints": {
            "auth": "/api/v1/auth",
            "patients": "/api/v1/patients",
            "psychologists": "/api/v1/psychologists",
            "appointments": "/api/v1/appointments",
            "requests": "/api/v1/requests",
            "reports": "/api/v1/reports",
            "ml_analysis": "/api/v1/ml"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )