from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from ml.predict import predict_book
from schemas import PredictionInput

router = APIRouter(prefix="/api/v1/ml", tags=["ML"])


@router.get("/training-data")
def get_training_data(db: Session = Depends(get_db)):
    books = db.query(Book).all()

    # Converte os dados para dicionário
    data = [
        {
            "price": book.price,
            "rating": book.rating,
            "availability": book.availability,
            #"category": book.category,
            # Exemplo de label: popularidade
            "popular": 1 if book.rating >= 4 else 0
        }
        for book in books
    ]

    return data

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


@router.post("/predictions")
def make_prediction(payload: PredictionInput):
    try:
        prediction = predict_book(payload)
        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}