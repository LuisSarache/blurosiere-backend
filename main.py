from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import os
from sqlalchemy import text
from sqlalchemy.orm import Session

#importacao da configuracao inicial do banco de dados
from core.database import get_db

load_dotenv()
app = FastAPI(
    title=os.getenv("APP_NAME"),
    version=os.getenv("APP_VERSION"),
)
@app.get("/")
def read_root():
    return {"message": "Bem-vindo a API Blurosiere"}

@app.get("/test-db")
def test_database_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"Status": "sucess", "message": "Conexão com banco de dados ok"}
    except Exception as error:
        return{"Status": "error", "message": f"falha na conexao: {error}"}