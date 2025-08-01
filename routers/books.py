from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, text
from database import SessionLocal
from models import Book
from schemas import BookBase
from typing import List, Optional
from database import get_db

router = APIRouter()


# 🟢 1. Listar todos os livros
@router.get("/api/v1/books", response_model=List[BookBase])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

# 🟢 2. Buscar por título e/ou categoria
@router.get("/api/v1/books/search", response_model=List[BookBase])
def search_books(title: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(Book.category.ilike(f"%{category}%"))
    return query.all()

# 🟢 3. Top 50 livros com melhor avaliação
@router.get("/api/v1/books/top-rated", response_model=List[BookBase])
def top_rated_books(db: Session = Depends(get_db)):
    return db.query(Book).order_by(desc(Book.rating)).limit(50).all()

# 🟢 4. Livros por faixa de preço
@router.get("/api/v1/books/price-range", response_model=List[BookBase])
def books_in_price_range(min_price: float, max_price: float, db: Session = Depends(get_db)):
    return db.query(Book).filter(and_(Book.price >= min_price, Book.price <= max_price)).all()

# 🟢 5. Detalhar um livro por ID
@router.get("/api/v1/books/{book_id}", response_model=BookBase)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book

# 🟢 6. Listar categorias únicas
@router.get("/api/v1/categories", response_model=List[str])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Book.category).distinct().all()
    return [c[0] for c in categories]

# 🟢 7. Verificar saúde da API
@router.get("/api/v1/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao conectar com o banco")

# 🟢 8. Estatísticas gerais
@router.get("/api/v1/stats/overview")
def stats_overview(db: Session = Depends(get_db)):
    total_books = db.query(func.count(Book.id)).scalar()
    avg_price = db.query(func.avg(Book.price)).scalar()
    rating_dist = db.query(Book.rating, func.count(Book.id)).group_by(Book.rating).all()
    return {
        "total_books": total_books,
        "avg_price": round(avg_price or 0, 2),
        "rating_distribution": [{"rating": r, "count": c} for r, c in rating_dist]
    }

# 🟢 9. Estatísticas por categoria
@router.get("/api/v1/stats/categories")
def stats_by_category(db: Session = Depends(get_db)):
    result = db.query(
        Book.category,
        func.count(Book.id).label("count"),
        func.avg(Book.price).label("avg_price")
    ).group_by(Book.category).all()
    return [{"category": cat, "count": count, "avg_price": round(avg, 2) if avg else 0} for cat, count, avg in result]

