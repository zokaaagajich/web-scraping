

import sys
import time

sys.path.append('../')

import audible_search_shared_methods as audible_shared
import helpers
from bs4 import BeautifulSoup

book_titles = []
book_authors = []
book_release_dates = []
book_prices = []

def main():
    start_time = time.time()
    website = 'https://www.audible.com/search'
    html = audible_shared.fetch_html(website)
    soup = BeautifulSoup(html, 'lxml')

    last_page = audible_shared.get_last_page(soup)

    for page in range(1, int(last_page) + 1):
        html = audible_shared.fetch_html(f'{website}?page={page}')
        soup = BeautifulSoup(html, 'lxml')
        container = soup.find('div', class_='adbl-impression-container')
        titles, authors, release_dates, prices = audible_shared.collect_books_info(container)
        book_titles.extend(titles)
        book_authors.extend(authors)
        book_release_dates.extend(release_dates)
        book_prices.extend(prices)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    helpers.export_data_as_csv('books-scraped-multiple-pages.csv', book_titles, book_authors, book_release_dates, book_prices)

if __name__ == "__main__":
    main()