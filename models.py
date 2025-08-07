"""
Modelo ORM para representar livros na tabela 'books'.

Cada instância de Book corresponde a um registro no banco de dados,
com campos como título, preço, disponibilidade, avaliação, etc.
"""

from sqlalchemy import Column, Integer, String, Float
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)  # ID único do livro
    title = Column(String, nullable=False)              # Título do livro
    price = Column(Float)                               # Preço em formato decimal
    availability = Column(String)                       # Disponibilidade ("In stock", etc.)
    rating = Column(Integer)                            # Avaliação (1 a 5 estrelas)
    category = Column(String)                           # Categoria/assunto do livro
    image = Column(String)                              # URL da imagem da capa
