import re
import sys

sys.path.append('../')

import helpers
import pandas as pd
import requests


def fetch_html(url):
    try: 
        response = requests.get(url) 
    except requests.exceptions.RequestException:
        print("Error fetching page")
        exit()    

    return response.text

def get_last_page(soup):
    pagination = soup.find('ul', class_='pagingElements')
    pages = pagination.find_all('li', class_='bc-list-item')
    return pages[-2].text

def collect_books_info(container) :
    book_titles = []
    book_authors = []
    book_release_dates = []
    book_prices = []

    book_list = container.find_all('li', class_='productListItem')
    for book in book_list:
        book_titles.append(book.find('h3', class_='bc-heading').text.strip())
        book_authors.append(book.find('li', class_='authorLabel').a.text.strip())
        book_release_dates.append(helpers.substr_after_colon(book.find('li', class_='releaseDateLabel').text.strip()))

        price_element = book.find('div', class_='adblBuyBoxPrice')
        if price_element is not None:
            book_prices.append(helpers.extract_regular_price(price_element.text.strip()))
        else:
            book_prices.append('-') 

    return book_titles, book_authors, book_release_dates, book_prices,