"""
Módulo de configuração do banco de dados utilizando SQLAlchemy.

Responsável por:
- Criar a conexão com o banco de dados.
- Definir a base declarativa para os modelos ORM.
- Fornecer a função `get_db` para injeção de dependência no FastAPI.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 📌 URL do banco de dados SQLite
DATABASE_URL = "sqlite:///./books.db"

# 🔌 Criação do engine (conexão com o banco)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 🛠️ Sessão para gerenciar transações no banco
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 🏗 Base para criação dos modelos ORM
Base = declarative_base()


def get_db():
    """
    Gera uma sessão de banco de dados para ser usada como dependência no FastAPI.
    Garante que a conexão será fechada após o uso.

    Yields:
        SessionLocal: Sessão ativa para operações no banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
