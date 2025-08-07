import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL base do site a ser raspado
BASE_URL = 'https://books.toscrape.com/'

# Mapeamento das classes de avaliação para valores numéricos
RATING_MAP = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

# Função para obter o conteúdo HTML de uma URL e retornar um objeto BeautifulSoup
def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Garante erro em caso de falha na requisição
    return BeautifulSoup(response.text, 'lxml')

# Função para extrair os dados relevantes de um livro, retornando um dicionário
def parse_book(book, category, book_id):
    title = book.h3.a['title']  # Título do livro
    price = float(book.select_one('.price_color').text.strip().lstrip('Â££'))  # Preço convertido para float
    availability = book.select_one('.availability').text.strip()  # Status de disponibilidade
    rating_text = book.select_one('p.star-rating')['class'][1]  # Texto da avaliação (ex: 'Three')
    rating = RATING_MAP.get(rating_text, 0)  # Converter texto para número
    image_url = urljoin(BASE_URL, book.img['src'].replace('../', ''))  # URL completa da imagem

    return {
        'id': book_id,
        'title': title,
        'price': price,
        'availability': availability,
        'rating': rating,
        'category': category,
        'image': image_url
    }

# Função para obter todas as categorias disponíveis no site, com suas URLs completas
def get_categories():
    soup = get_soup(BASE_URL)
    categories = soup.select('.side_categories ul li ul li a')
    return {cat.text.strip(): urljoin(BASE_URL, cat['href']) for cat in categories}

# Função principal que realiza a raspagem de todos os livros em todas as categorias
def scrape_all_books():
    books_data = []  # Lista para armazenar os dados de todos os livros
    categories = get_categories()  # Obtém categorias e URLs
    total_categories = len(categories)
    book_id = 1  # ID sequencial para cada livro

    # Loop por cada categoria, com índice para controle de progresso
    for idx_cat, (category, url) in enumerate(categories.items(), start=1):
        print(f"🔍 Raspando categoria {idx_cat}/{total_categories}: {category}")
        page_url = url

        # Loop para percorrer todas as páginas dentro da categoria
        while page_url:
            soup = get_soup(page_url)
            books = soup.select('article.product_pod')  # Seleciona todos os livros da página

            # Extrai e armazena os dados de cada livro
            for book in books:
                books_data.append(parse_book(book, category, book_id))
                book_id += 1

            # Verifica se existe próxima página; atualiza URL ou encerra o loop
            next_btn = soup.select_one('li.next > a')
            page_url = urljoin(page_url, next_btn['href']) if next_btn else None

        print(f"✅ Finalizada categoria '{category}' ({idx_cat}/{total_categories})")

    return books_data, sorted(categories.keys())

# Bloco principal de execução, só rodado quando o script é executado diretamente
if __name__ == "__main__":
    books, categories = scrape_all_books()

    print(f'\n📚 Total de livros encontrados: {len(books)}')
    print(f'📂 Total de categorias: {len(categories)}\n')

    print("📘 Primeiro livro:")
    print(books[0] if books else "Nenhum livro encontrado.")

    print("\n📂 Categorias:")
    print(categories)
