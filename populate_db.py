from scraper import scrape_all_books
from database import SessionLocal
from models import Book

db = SessionLocal()
books, _ = scrape_all_books()
total = len(books)

print(f"🔄 Iniciando inserção de {total} livros...\n")

for idx, b in enumerate(books, start=1):
    book = Book(**b)
    db.merge(book)

    # Mostrar progresso a cada 5% ou no fim
    percentage = (idx / total) * 100
    if idx == total or int(percentage) % 5 == 0 and (idx == 1 or int(((idx - 1) / total) * 100) != int(percentage)):
        print(f"📊 Progresso: {percentage:.1f}% ({idx}/{total})")

db.commit()
db.close()

print("\n✅ Todos os dados foram inseridos com sucesso!")
