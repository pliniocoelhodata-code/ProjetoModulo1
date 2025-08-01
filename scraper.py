import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'https://books.toscrape.com/'

RATING_MAP = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')

def parse_book(book, category, book_id):
    title = book.h3.a['title']
    price = float(book.select_one('.price_color').text.strip().lstrip('Â££'))
    availability = book.select_one('.availability').text.strip()
    rating_text = book.select_one('p.star-rating')['class'][1]
    rating = RATING_MAP.get(rating_text, 0)
    image_url = urljoin(BASE_URL, book.img['src'].replace('../', ''))

    return {
        'id': book_id,
        'title': title,
        'price': price,
        'availability': availability,
        'rating': rating,
        'category': category,
        'image': image_url
    }

def get_categories():
    soup = get_soup(BASE_URL)
    categories = soup.select('.side_categories ul li ul li a')
    return {cat.text.strip(): urljoin(BASE_URL, cat['href']) for cat in categories}

def scrape_all_books():
    books_data = []
    categories = get_categories()
    book_id = 1

    for category, url in categories.items():
        page_url = url
        while page_url:
            soup = get_soup(page_url)
            books = soup.select('article.product_pod')

            for book in books:
                books_data.append(parse_book(book, category, book_id))
                book_id += 1

            next_btn = soup.select_one('li.next > a')
            page_url = urljoin(page_url, next_btn['href']) if next_btn else None

    return books_data, sorted(categories.keys())


"""if __name__ == '__main__':
    books, categories = scrape_all_books()

    print(f'Total de livros encontrados: {len(books)}')
    print(f'Total de categorias: {len(categories)}\n')

    print("📘 Primeiro livro:")
    print(books[0])

    print("\n📂 Categorias:")
    print(categories)
"""