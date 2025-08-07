from pydantic import BaseModel

# 📚 Modelo base para representar os dados de um livro
class BookBase(BaseModel):
    id: int               # Identificador único do livro
    title: str            # Título do livro
    price: float          # Preço do livro
    availability: str     # Status de disponibilidade (ex.: "In stock")
    rating: int           # Avaliação (ex.: 1 a 5 estrelas)
    category: str         # Categoria do livro
    image: str            # URL da imagem da capa

    class Config:
        # 🛠️ Permite que o Pydantic crie modelos a partir de objetos ORM (ex: SQLAlchemy)
        orm_mode = True


# 🔮 Modelo para receber os dados de entrada da previsão
class PredictionInput(BaseModel):
    price: float          # Preço do livro para a previsão
    rating: int           # Avaliação do livro para a previsão
    availability: str     # Disponibilidade para a previsão ("In stock" / "Out of stock")
