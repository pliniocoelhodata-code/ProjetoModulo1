"""
Script para inicializar o banco de dados e criar as tabelas definidas nos modelos ORM.
"""

from database import engine
from models import Base

def init_database():
    """
    Cria todas as tabelas no banco de dados, baseadas nos modelos ORM definidos.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados e tabelas criados com sucesso.")

if __name__ == "__main__":
    init_database()
