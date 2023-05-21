

import sys

sys.path.append('../')

import time

import audible_search_shared_methods as audible_shared
import helpers
from bs4 import BeautifulSoup


def main():
    start_time = time.time()
    html = audible_shared.fetch_html('https://www.audible.com/search')
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.text)
    # print(soup.title.text)

    container = soup.find('div', class_='adbl-impression-container')
    book_titles, book_authors, book_release_dates, book_prices = audible_shared.collect_books_info(container)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    helpers.export_data_as_csv('books-scraped-single-page.csv', book_titles, book_authors, book_release_dates, book_prices)

if __name__ == "__main__":
    main()