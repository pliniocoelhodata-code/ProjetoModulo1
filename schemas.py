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
        from_attributes = True


class PredictionInput(BaseModel):
    price: float
    rating: int
    availability: str
    
