"""
Script para popular o banco de dados com livros coletados via web scraping.

Executa:
- Extração de livros com `scrape_all_books`
- Inserção ou atualização com `db.merge`
"""

from scraper import scrape_all_books
from database import SessionLocal
from models import Book

def main():
    db = SessionLocal()

    try:
        books, _ = scrape_all_books()
        total = len(books)

        print(f"🔄 Iniciando inserção de {total} livros...\n")

        for b in books:
            book = Book(**b)
            db.merge(book)

        db.commit()
        print("✅ Todos os dados foram inseridos com sucesso!")

    finally:
        db.close()


if __name__ == "__main__":
    main()
