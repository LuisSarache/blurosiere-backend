"""
Configurações centralizadas da aplicação Blurosiere
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Aplicação
    app_name: str = "Blurosiere API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Segurança
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # Banco de dados
    database_url: str = "sqlite:///./blurosiere.db"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Machine Learning
    ml_model_path: str = "./models/"
    risk_threshold_high: int = 70
    risk_threshold_moderate: int = 40
    
    @field_validator('cors_origins')
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        """Converte string de origens CORS em lista"""
        return [origin.strip() for origin in v.split(",")]
    
    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Valida se a chave secreta tem tamanho mínimo"""
        if len(v) < 32:
            raise ValueError('SECRET_KEY deve ter pelo menos 32 caracteres')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global das configurações
settings = Settings()