from pydantic import BaseModel

class BookBase(BaseModel):
    id: int
    title: str
    price: float
    availability: str
    rating: int
    category: str
    image: str


    class Config:
        # Permite criar instâncias do Pydantic a partir de objetos ORM (ex.: SQLAlchemy)
        orm_mode = True


class PredictionInput(BaseModel):
    price: float
    rating: int
    availability: str
    
