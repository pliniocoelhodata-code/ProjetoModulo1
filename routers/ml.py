from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from ml.predict import predict_book
from schemas import PredictionInput

router = APIRouter(prefix="/api/v1/ml", tags=["ML"])

# 📊 Rota para obter dados usados no treinamento do modelo
@router.get("/training-data")
def get_training_data(db: Session = Depends(get_db)):
    books = db.query(Book).all()

    data = [
        {
            "price": book.price,
            "rating": book.rating,
            "availability": book.availability,
            "popular": 1 if book.rating >= 4 else 0  # Rótulo baseado na avaliação
        }
        for book in books
    ]

    return data

# 🧠 Rota para extrair as features do modelo de ML
@router.get("/features")
def get_ml_features(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    features = []

    for book in books:
        features.append({
            "price": book.price,
            "rating": book.rating,
            "availability": 1 if "In stock" in (book.availability or "") else 0,
            "category": book.category
        })

    return {"features": features}

# 🔮 Rota para fazer previsão de popularidade com base nas features fornecidas
@router.post("/predictions")
def make_prediction(payload: PredictionInput):
    try:
        prediction = predict_book(payload)
        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}
